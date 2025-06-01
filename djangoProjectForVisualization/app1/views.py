import torch

from app1.TrafficPrediction.src.traffic_prediction import all_predict_values, test_loader, first_data, all_data
from app1.api.submit import submit_json
from django.http import JsonResponse
from app1.TrafficPrediction.src.vue_traffic_prediction import predict
# from app1.TrafficPrediction.src.vue_traffic_prediction import predict
# Create your views here.


def test(request):
    print(all_data)
    race_json_data = []
    json_data = submit_json(all_data)

    dimension = ['Predict', 'Group', 'Time']
    race_json_data.append(dimension)
    for j in range(0, 288 * 2, 12):
        for i in range(0, 7):
            average_predict = 0
            for k in range(12):
                average_predict += int(json_data["node_flow"][i][i * 5 * 288 * 2 + (j + k) * 5])
            tmp = [int(average_predict / 12), f"Group_{i}", j * 5 / 60]
            race_json_data.append(tmp)

    return JsonResponse(race_json_data, safe=False)


# 返回模型所计算的前端上传的数据文件的结果
def get_res(request):
    all_datas = predict()
    new_one_week_data1 = all_datas[:2016]
    new_one_week_data2 = all_datas[2016:]
    days_data1 = new_one_week_data1.view(7, 288)
    days_data2 = new_one_week_data2.view(7, 288)
    results1 = []
    results2 = []
    for i in range(7):
        daily_value1 = days_data1[i].mean().item()
        daily_value2 = days_data2[i].mean().item()

        results1.append({"name": f"第{i + 1}天", "value": daily_value1})
        results2.append({"name": f"第{i + 1}天", "value": daily_value2})
    # print(results)
    results = {'1':results1, '2':results2}
    return JsonResponse(results, safe=False)


def getTwo_week(request):
    one_week_data = all_data[:2016]
    # 如何将其返回去？
    days_data = one_week_data.view(7, 288)
    results = []
    for i in range(7):
        daily_value = days_data[i].mean().item()
        results.append({"name": f"第{i + 1}天", "value": daily_value})
    print(results)

    return JsonResponse(results, safe=False)

def getOne_week(request):
    one_week_data = all_data[2016:]
    # 如何将其返回去？
    days_data = one_week_data.view(7, 288)

    results = []


    for i in range(7):
        daily_value = days_data[i].mean().item()
        results.append({"name": f"第{i + 1}天", "value": daily_value})
    print(results)

    return JsonResponse(results, safe=False)





