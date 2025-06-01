import time
import random
import json

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

import matplotlib.pyplot as plt

from .data_loader import get_loader

from .data_loader import vue_get_loader
from .model import GCN
from .visualize_dataset import show_pred

seed = 200

random.seed(seed)
torch.manual_seed(seed)
np.random.seed(seed)

plt.rcParams['font.sans-serif'] = ['simhei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# train_loader, test_loader = get_loader('data')  # 提交上来的文件称为data

gcn = GCN(6, 6, 1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def predict():
    test_loader = vue_get_loader()
    model = gcn.to(device)
    predict_values = []
    epochs = 30
    model.eval()
    criterion = nn.MSELoss().to(device)

    total_loss = 0.0
    num = 0
    all_y_true = 0
    all_predict_value = 0
    checkpoint = torch.load('app1/TrafficPrediction/params/model_1_params.pth')
    model.load_state_dict(checkpoint)
    with torch.no_grad():
        for data in test_loader:
            data['graph'], data['flow_x'], data['flow_y'] = data['graph'].to(device), data['flow_x'].to(device), \
                data['flow_y'].to(device)
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

        # print('predict_value',all_predict_value)
        predict_values.append(all_predict_value.cpu())

    # show_pred(test_loader, all_y_true.cpu(), predict_values)

    all_data = test_loader.dataset.recover_data(test_loader.dataset.flow_norm[0], test_loader.dataset.flow_norm[1],
                                                predict_values[0])[:, 1, 0, 0]
    return all_data
















