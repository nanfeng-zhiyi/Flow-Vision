import json


# 这里是返回第一天的道路节点流量预测结果
def submit_json(first_data):
    data_dict = {
        "node_flow": []
    }
    for i in range(int(len(first_data) / (288 * 2))):
        tmp = {j * 5: float(first_data[j]) for j in range(i * 288 * 2, (i + 1) * 288 * 2)}
        data_dict["node_flow"].append(tmp)

    return data_dict


