import math
import os.path
import pandas as pd
import numpy as np
import arcpy


def remove_spaces_from_list(input_list):
    result_list = []
    for item in input_list:
        if isinstance(item, str):
            cleaned_item = item.replace(" ", "")
            result_list.append(cleaned_item)
        else:
            result_list.append(item)
    return result_list


folder = 'C:/Users/zmyzq/Desktop/台风/CMABSTdata'

file_name = os.listdir(folder)

all_lines = []

for i in file_name:
    ph = os.path.join(folder, i)
    source = open(ph, 'r')
    hhh = source.readlines()
    all_lines = all_lines + hhh

dataset = []
for line in all_lines:
    line = line.strip().split('\t')
    dataset.append(line)
df = pd.DataFrame(dataset)

Typhoon_Name = []
Typhoon_time = []
Typhoon_record_num = []
Typhoon_record_time = []
Typhoon_grade = []
Typhoon_coord_lat = []
Typhoon_coord_long = []
Typhoon_pres = []
Typhoon_wnd = []

item = 0
for i in df[0]:
    if '66666' in i:
        Typhoon_Name.append(i[30:50])
        Typhoon_record_num.append(int(i[12:15]))
        Typhoon_record_time.append(list())
        Typhoon_grade.append(list())
        Typhoon_coord_lat.append(list())
        Typhoon_coord_long.append(list())
        Typhoon_pres.append(list())
        Typhoon_wnd.append(list())
        item += 1
        record = 0
    else:
        Typhoon_record_time[item - 1].append(int(i[0:10]))
        Typhoon_grade[item - 1].append(int(i[11]))
        Typhoon_coord_lat[item - 1].append(int(i[13:16])/10)
        Typhoon_coord_long[item - 1].append(int(i[17:21])/10)
        Typhoon_pres[item - 1].append(int(i[22:26]))
        Typhoon_wnd[item - 1].append(int(i[32:34]))
        record += 1
Typhoon_Name = remove_spaces_from_list(Typhoon_Name)
Typhoon_record_time = [i[0] for i in Typhoon_record_time]

# 设置工作空间
arcpy.env.workspace = r"D:\临灾评估\台风\BST"

# 创建要素类
output_fc = r"D:\临灾评估\台风\BST/lines.shp"
spatial_reference = arcpy.SpatialReference(4326)
arcpy.CreateFeatureclass_management(r"D:\临灾评估\台风\BST", "lines.shp", "POLYLINE", spatial_reference=spatial_reference)


field_names = ["Name", "Length", "Time"]
field_types = ["TEXT", "DOUBLE", "DOUBLE"]

# 添加字段到要素类
for field_name, field_type in zip(field_names, field_types):
    arcpy.AddField_management(output_fc, field_name, field_type)

lon_list = Typhoon_coord_long
lat_list = Typhoon_coord_lat

# 创建多条线要素
with arcpy.da.InsertCursor(output_fc, ["SHAPE@", "Name", "Length", "Time"]) as cursor:
    for i in range(len(lon_list)):
        line_coords = zip(lon_list[i], lat_list[i])
        polyline = arcpy.Polyline(arcpy.Array([arcpy.Point(lon, lat) for lon, lat in line_coords]), spatial_reference)
        name = Typhoon_Name[i]
        length = polyline.length
        time = Typhoon_record_time[i]
        cursor.insertRow([polyline, name, length, time])

print("多条线要素以Shapefile格式保存成功。")
