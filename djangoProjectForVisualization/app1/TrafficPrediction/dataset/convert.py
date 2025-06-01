# import geopandas as gpd
#
# # 加载Shapefile
# gdf = gpd.read_file('./【立方数据学社】295地级市公路里程.shp')
#
# # 输出GeoJSON
# gdf.to_file("./geoData.geojson", driver='GeoJSON')
#
# # 打印GeoJSON内容（可选）
# print(gdf.to_json())

import geopandas as gpd
import json

# 载入GeoJSON文件
gdf = gpd.read_file("./geoData.geojson")

data_list = []  # 存储所有城市的数据

for index, row in gdf.iterrows():
    city_name = row['city']  # 城市名称存储在 'city' 属性中
    km_key = "2020年"
    km_value = row[km_key] if km_key in row else 0  # 读取2020年的道路里程数，如果没有数据则设为 None

    # 构造字典并添加到列表
    data_list.append({"name": city_name, "value": km_value})


# 将数据写入JSON文件
with open('outputData.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)  # 美化输出，便于阅读

