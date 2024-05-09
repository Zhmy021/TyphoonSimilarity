from math import *


def typhoonLand(typhoonName):
    import math
    import os.path
    import pandas as pd
    import numpy as np
    import pyproj

    def remove_spaces_from_list(input_list):
        result_list = []
        for item in input_list:
            if isinstance(item, str):
                cleaned_item = item.replace(" ", "")
                result_list.append(cleaned_item)
            else:
                result_list.append(item)
        return result_list

    def min_max_normalize(data):
        min_value = min(data)
        max_value = max(data)
        normalized_data = [(x - min_value) / (max_value - min_value) for x in data]
        return normalized_data

    def geodetic_to_gauss_kruger(latitude, longitude):
        # 定义投影坐标系，zone 参数是高斯-克吕格投影的带号，范围是1到60
        proj = pyproj.Proj(proj="utm", zone=51, ellps="WGS84")

        # 将地理坐标转换为高斯平面直角坐标
        easting, northing = proj(longitude, latitude)

        return easting, northing

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
            Typhoon_coord_lat[item - 1].append(int(i[13:16]))
            Typhoon_coord_long[item - 1].append(int(i[17:21]))
            Typhoon_pres[item - 1].append(int(i[22:26]))
            Typhoon_wnd[item - 1].append(int(i[32:34]))
            record += 1
    Typhoon_Name = remove_spaces_from_list(Typhoon_Name)
    Typhoon_record_time = [i[0] for i in Typhoon_record_time]
    rectangular_coordinates_X = []
    rectangular_coordinates_Y = []

    for i in range(len(Typhoon_coord_lat)):
        rectangular_coordinates_X.append(list())
        rectangular_coordinates_Y.append(list())
        for j in range(len(Typhoon_coord_lat[i])):
            qqq = [Typhoon_coord_long[i][j] / 10, Typhoon_coord_lat[i][j] / 10]
            qwer = geodetic_to_gauss_kruger(Typhoon_coord_lat[i][j] / 10, Typhoon_coord_long[i][j] / 10)
            rectangular_coordinates_X[i].append(qwer[0])
            rectangular_coordinates_Y[i].append(qwer[1])

    rectangular_coordinates_X_use = []
    rectangular_coordinates_Y_use = []
    N = len(Typhoon_coord_lat)  # N表示所取台风个数
    for i in range(len(Typhoon_coord_lat)):
        rectangular_coordinates_X_use.append(rectangular_coordinates_X[i][-9:])
        rectangular_coordinates_Y_use.append(rectangular_coordinates_Y[i][-9:])

    SUM_Y = []  # 储存控制点纵坐标差
    SUM_X = []
    SUM_D = []  # 储存纵坐标差与平均值的差
    Sim_distance = {}

    D_ij = [0 for i in range(len(Typhoon_coord_lat))]  # D_ij表示台风纵坐标平均距离
    S_ij = [0 for i in range(len(Typhoon_coord_lat))]  # S_ij表示台风路径形状系数
    C_ij = [0 for i in range(len(Typhoon_coord_lat))]  # C_ij表示台风间的相似离度，越小表示台风间越相似

    y = rectangular_coordinates_Y_use  # y[i][j]表示所求第i条台风的第j个控制点的纵坐标
    x = rectangular_coordinates_X_use

    target_X = rectangular_coordinates_X_use[-1]
    target_Y = rectangular_coordinates_Y_use[-1]

    sss = 0
    for i in range(N):
        SUM_Y.append([])
        SUM_X.append([])
        if len(y[i]) >= 9:
            for j in range(9):
                SUM_Y[i].append(math.fabs(target_Y[j] - y[i][j]))  # 计算控制点纵坐标差
                SUM_X[i].append(math.fabs(target_X[j] - x[i][j]))  # 计算控制点纵坐标差
    print(N)
    for i in range(N):
        SUM_D.append(0)
        if len(y[i]) >= 9:
            for j in range(9):
                SUM_D[i] += math.fabs(sqrt(int(target_Y[j] - y[i][j]) ** 2 + int(target_X[j] - x[i][j]) ** 2) - D_ij[i])
                D_ij[i] += sqrt((SUM_Y[i][j] ** 2) + (SUM_X[i][j] ** 2)) / 9

                # 计算纵坐标差与平均值的差，与台风纵坐标平均距离
        else:
            for j in range(len(y[i])):
                SUM_D[i] += 0

    for i in range(N):
        if len(y[i]) >= 9:
            for j in range(9):
                SUM_D[i] += math.fabs(sqrt(int(target_Y[j] - y[i][j]) ** 2 + int(target_X[j] - x[i][j]) ** 2) - D_ij[i])
                S_ij[i] += (sqrt((SUM_Y[i][j] ** 2) + (SUM_X[i][j] ** 2)) - D_ij[i]) / 9  # 计算台风路径形状系数

    D_ij = min_max_normalize(D_ij)
    S_ij = min_max_normalize(S_ij)
    for i in range(N):
        C_ij[i] = 0.7 * D_ij[i] + 0.3 * S_ij[i]  # 计算台风间的相似离度
        Sim_distance[Typhoon_Name[i].strip()] = [C_ij[i], Typhoon_record_time[i], S_ij[i], D_ij[i], C_ij[i]]

    a = sorted(Sim_distance.items(), key=lambda x: x[1])
    result = [[], {}]
    for key, value in a:
        if value[0] != 0 and value[3] != 0:
            print(key, value, '\n')
            result[0].append([key, value[1]])
            result[1][key] = value
    print(result)
    return result


typhoonLand('Ophelia')
