import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init


class GCN(nn.Module):
    def __init__(self, in_c, hid_c, out_c):
        """
        初始化函数
        :param in_c: 输入通道数
        :param hid_c: 隐藏层节点数
        :param out_c: 输出通道数
        """
        super(GCN, self).__init__()
        # 定义第一个线性变换层
        self.linear_1 = nn.Linear(in_c, hid_c)
        # 定义第二个线性变换层
        self.linear_2 = nn.Linear(hid_c, out_c)
        # 定义ReLU激活函数
        self.act = nn.ReLU()

    def forward(self, data):
        # 获取图的邻接矩阵
        graph_data = data["graph"][0]  # [N, N]
        # 处理图的邻接矩阵，包括添加自环和标准化
        graph_data = self.process_graph(graph_data)
        # 获取流量数据
        flow_x = data["flow_x"]  # [B, N, H, D]
        # 提取batch大小和节点数量
        B, N = flow_x.size(0), flow_x.size(1)
        # 重塑流量数据以匹配网络输入
        flow_x = flow_x.view(B, N, -1)  # [B, N, H*D]  H = 6, D = 1
        # 应用第一个线性变换和激活函数
        output_1 = self.linear_1(flow_x)  # [B, N, hid_C]
        output_1 = self.act(torch.matmul(graph_data, output_1))  # [N, N] * [B, N, Hid_C]
        # 应用第二个线性变换和激活函数
        output_2 = self.linear_2(output_1)
        output_2 = self.act(torch.matmul(graph_data, output_2))  # [B, N, Out_C]

        # 返回最终结果，增加一个新的维度
        return output_2.unsqueeze(2)

    @staticmethod
    def process_graph(graph_data):
        # 获取节点数量
        N = graph_data.size(0)
        # 创建单位矩阵
        matrix_i = torch.eye(N, dtype=graph_data.dtype, device=graph_data.device)
        # 为邻接矩阵添加自环
        graph_data += matrix_i  # A~ [N, N]
        # 创建度矩阵
        degree_matrix = torch.sum(graph_data, dim=-1, keepdim=False)  # [N]
        # 计算度矩阵的逆，处理inf为0
        degree_matrix = degree_matrix.pow(-1)
        degree_matrix[degree_matrix == float("inf")] = 0.  # [N]
        # 构建对角度矩阵
        degree_matrix = torch.diag(degree_matrix)  # [N, N]
        # 返回标准化的邻接矩阵
        return torch.mm(degree_matrix, graph_data)  # D^(-1) * A = \hat(A)


class ChebConv(nn.Module):

    def __init__(self, in_c, out_c, K, bias=True, normalize=True):

        super(ChebConv, self).__init__()
        self.normalize = normalize

        self.weight = nn.Parameter(torch.Tensor(K + 1, 1, in_c, out_c))  # [K+1, 1, in_c, out_c]
        init.xavier_normal_(self.weight)

        if bias:
            self.bias = nn.Parameter(torch.Tensor(1, 1, out_c))
            init.zeros_(self.bias)
        else:
            self.register_parameter("bias", None)

        self.K = K + 1

    def forward(self, inputs, graph):

        L = ChebConv.get_laplacian(graph, self.normalize)  # [N, N]
        mul_L = self.cheb_polynomial(L).unsqueeze(1)  # [K, 1, N, N]
        result = torch.matmul(mul_L, inputs)  # [K, B, N, C]
        result = torch.matmul(result, self.weight)  # [K, B, N, D]
        result = torch.sum(result, dim=0) + self.bias  # [B, N, D]

        return result

    def cheb_polynomial(self, laplacian):

        N = laplacian.size(0)  # [N, N]
        multi_order_laplacian = torch.zeros([self.K, N, N], device=laplacian.device, dtype=torch.float)  # [K, N, N]
        multi_order_laplacian[0] = torch.eye(N, device=laplacian.device, dtype=torch.float)

        if self.K == 1:
            return multi_order_laplacian
        else:
            multi_order_laplacian[1] = laplacian
            if self.K == 2:
                return multi_order_laplacian
            else:
                for k in range(2, self.K):
                    multi_order_laplacian[k] = 2 * torch.mm(laplacian, multi_order_laplacian[k - 1]) - \
                                               multi_order_laplacian[k - 2]

        return multi_order_laplacian

    @staticmethod
    def get_laplacian(graph, normalize):

        if normalize:
            D = torch.diag(torch.sum(graph, dim=-1) ** (-1 / 2))
            L = torch.eye(graph.size(0), device=graph.device, dtype=graph.dtype) - torch.mm(torch.mm(D, graph), D)
        else:
            D = torch.diag(torch.sum(graph, dim=-1))
            L = D - graph
        return L


class ChebNet(nn.Module):

    def __init__(self, in_c, hid_c, out_c, K):

        super(ChebNet, self).__init__()
        self.conv1 = ChebConv(in_c=in_c, out_c=hid_c, K=K)
        self.conv2 = ChebConv(in_c=hid_c, out_c=out_c, K=K)
        self.act = nn.ReLU()

    def forward(self, data):
        graph_data = data["graph"][0]  # [N, N]
        flow_x = data["flow_x"]  # [B, N, H, D]

        B, N = flow_x.size(0), flow_x.size(1)

        flow_x = flow_x.view(B, N, -1)  # [B, N, H*D]

        output_1 = self.act(self.conv1(flow_x, graph_data))
        output_2 = self.act(self.conv2(output_1, graph_data))

        return output_2.unsqueeze(2)


class GraphAttentionLayer(nn.Module):
    def __init__(self, in_c, out_c, alpha=0.2):
        """
        图注意力层的初始化
        :param in_c: 输入特征的维度
        :param out_c: 输出特征的维度
        :param alpha: LeakyReLU激活函数中的负斜率
        """
        super(GraphAttentionLayer, self).__init__()
        self.in_c = in_c
        self.out_c = out_c
        self.alpha = alpha

        # 初始化权重矩阵W和注意力系数向量a
        self.W = nn.Parameter(torch.empty(size=(in_c, out_c)))
        init.xavier_normal_(self.W.data)
        self.a = nn.Parameter(torch.empty(size=(2 * out_c, 1)))
        init.xavier_normal_(self.a.data)

        # 定义LeakyReLU激活函数
        self.leakyrelu = nn.LeakyReLU(self.alpha)

    def forward(self, features, adj):
        """
        前向传播
        :param features: 输入特征
        :param adj: 邻接矩阵
        """
        B, N = features.size(0), features.size(1)
        # 通过权重矩阵W对特征进行变换
        h = torch.matmul(features, self.W)  # [B,N,out_features]

        # 准备求取注意力系数
        a_input = torch.cat([h.repeat(1, 1, N).view(B, N * N, -1), h.repeat(1, N, 1)], dim=2).view(B, N, -1,
                                                                                                   2 * self.out_c)
        e = self.leakyrelu(torch.matmul(a_input, self.a).squeeze(3))  # [B,N, N, 1] => [B, N, N]

        # 使用softmax函数归一化得到节点间的注意力系数
        attention = F.softmax(e, dim=2)  # [B, N, N]

        # 计算加权的节点特征
        h_prime = torch.matmul(attention, h)  # [B,N, N]*[B,N, out_features] => [B,N, out_features]
        return h_prime

    def __repr__(self):
        """
        字符串表示
        """
        return self.__class__.__name__ + ' (' + str(self.in_features) + ' -> ' + str(self.out_features) + ')'


class GAT(nn.Module):
    def __init__(self, in_c, hid_c, out_c, n_heads=6):

        super(GAT, self).__init__()
        self.attentions = nn.ModuleList([GraphAttentionLayer(in_c, hid_c) for _ in range(n_heads)])
        self.conv2 = GraphAttentionLayer(hid_c*n_heads, out_c)
        self.act = nn.ELU()

    def forward(self, data):
        # dataset prepare
        adj = data["graph"][0]  # [N, N]
        x = data["flow_x"]  # [B, N, H, D]
        B, N = x.size(0), x.size(1)
        x = x.view(B, N, -1)  # [B, N, H*D]

        # forward
        outputs = self.act(torch.cat([attention(x, adj) for attention in self.attentions], dim=-1))
        output_2 = self.act(self.conv2(outputs, adj))

        return output_2.unsqueeze(2)  # [B,1,N,1]

