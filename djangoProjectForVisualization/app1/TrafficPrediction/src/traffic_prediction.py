import time
import random
import json

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

import matplotlib.pyplot as plt

from .model import GCN, ChebNet, GAT
from .metrics import MAE, MAPE, RMSE
from .data_loader import get_loader
from .visualize_dataset import show_pred
from .data_loader import check_file_existence

seed = 2020
random.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)

plt.rcParams['font.sans-serif'] = ['simhei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# dataset
train_loader, test_loader = get_loader('PEMS04')

gcn = GCN(6, 6, 1)
chebnet = ChebNet(6, 6, 1, 1)
gat = GAT(6, 6, 1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
models = [
    chebnet.to(device),
    gcn.to(device),
    gat.to(device)
]

all_predict_values = []
epochs = 30
for i in range(len(models)):
    model = models[i]
    criterion = nn.MSELoss().to(device)
    optimizer = optim.Adam(params=model.parameters(), lr=3e-2)
    model.train()
    # 如果已经是预训练模型直接使用即可
    for epoch in range(epochs):
        if check_file_existence('app1/TrafficPrediction/params', f'model_{i}_params.pth'):
            checkpoint = torch.load(f'app1/TrafficPrediction/params/model_{i}_params.pth')
            model.load_state_dict(checkpoint)
            continue
        epoch_loss, epoch_mae, epoch_rmse, epoch_mape = 0.0, 0.0, 0.0, 0.0
        num = 0
        start_time = time.time()
        for data in train_loader:  # ["graph": [B, N, N] , "flow_x": [B, N, H, D], "flow_y": [B, N, 1, D]]
            data['graph'], data['flow_x'], data['flow_y'] = data['graph'].to(device), data['flow_x'].to(device), data['flow_y'].to(device)
            predict_value = model(data)  # [0, 1] -> recover
            loss = criterion(predict_value, data["flow_y"])
            epoch_mae += MAE(data["flow_y"].cpu(), predict_value.cpu())
            epoch_rmse += RMSE(data["flow_y"].cpu(), predict_value.cpu())
            epoch_mape += MAPE(data["flow_y"].cpu(), predict_value.cpu())

            epoch_loss += loss.item()
            num += 1
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        end_time = time.time()
        epoch_mae = epoch_mae / num
        epoch_rmse = epoch_rmse / num
        epoch_mape = epoch_mape / num
        print(
            "Epoch: {:04d}, Loss: {:02.4f}, mae: {:02.4f}, rmse: {:02.4f}, mape: {:02.4f}, Time: {:02.2f} mins".format(
                epoch + 1, 10 * epoch_loss / (len(train_loader.dataset) / 64),
                epoch_mae, epoch_rmse, epoch_mape, (end_time - start_time) / 60))
        if epoch == 29:
            torch.save(model.state_dict(),f'../params/model_{i}_params.pth')

    model.eval()  # 模型的评估
    with torch.no_grad():
        total_loss = 0.0
        num = 0
        all_predict_value = 0
        all_y_true = 0
        for data in test_loader:
            data['graph'], data['flow_x'], data['flow_y'] = data['graph'].to(device), data['flow_x'].to(device), data['flow_y'].to(device)
            predict_value = model(data)
            if num == 0:
                all_predict_value = predict_value
                all_y_true = data["flow_y"]
            else:
                all_predict_value = torch.cat([all_predict_value, predict_value], dim=0)
                all_y_true = torch.cat([all_y_true, data["flow_y"]], dim=0)
            loss = criterion(predict_value, data["flow_y"])
            total_loss += loss.item()
            num += 1
        epoch_mae = MAE(all_y_true.cpu(), all_predict_value.cpu())
        epoch_rmse = RMSE(all_y_true.cpu(), all_predict_value.cpu())
        epoch_mape = MAPE(all_y_true.cpu(), all_predict_value.cpu())
        print(all_predict_value.cpu().numpy().reshape((-1,1)))
        # df = pd.DataFrame(all_predict_value.cpu().numpy(), columns=['预测流量'])
        # df.to_csv('预测结果.csv', index=False)
        print("Test Loss: {:02.4f}, mae: {:02.4f}, rmse: {:02.4f}, mape: {:02.4f}".format(
            10 * total_loss / (len(test_loader.dataset) / 64), epoch_mae, epoch_rmse, epoch_mape))

    all_predict_values.append(all_predict_value.cpu())
show_pred(test_loader, all_y_true.cpu(), all_predict_values)

print(test_loader.dataset.recover_data(test_loader.dataset.flow_norm[0], test_loader.dataset.flow_norm[1],
                                       all_predict_values[0])[100:150,166,0,0])

##################################################################
first_data = test_loader.dataset.recover_data(test_loader.dataset.flow_norm[0], test_loader.dataset.flow_norm[1],
                                       all_predict_values[0])[:24*12,166,0,0]

all_data = test_loader.dataset.recover_data(test_loader.dataset.flow_norm[0], test_loader.dataset.flow_norm[1],
                                       all_predict_values[0])[:,166,0,0]
# 横坐标是时间步共288个每一个时间步相当于5分钟，同时包含每一个时间节点也就是每隔五分钟的该节点的流量
# 这里的all_preditct_values包含了三个预训练模型的预测结果， 这里我们默认使用第一个， 要使用归一化的最小值和最大值回复流量初始值上面的
# first_data是相应节点（这里设置为166）， 的单日流量数据, all_data 就是对应整个时间跨步的流量数据（一共两周），
# 这里的一个时间步是5分钟就是你所看到的[:24*12,166,0,0]， 这里你只需要观察前两个维度即可， 第一个是时间步和上面讲的一样
# 第二个维度是节点标号（就是数据集中构图中的图节点）
# 目前需要做的任务就是： 将我上面定义的数据传输到前端中（按照Details中的右侧两张图是进行数据展示）， 如果需要格式的调整自行修改即可
# 还有就是将plot画出的图示传输到前端， 再点击“显示结果”按钮之后会显示这两张结果图示
# plt.savefig("app1/TrafficPrediction/assets/the first two weeks pred flow in node {}.png".format(str(node_id)), dpi=400)
# 这是存储的路径，你可以再visualize_dataset.py文件中找到相应的代码

# 这里是输出的时间
data_dict = {
    "node_flow": {i * 5: float(first_data[i]) for i in range(len(first_data))}
}

json_data = json.dumps(data_dict)

print(json_data)



