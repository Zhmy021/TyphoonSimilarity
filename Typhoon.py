import pyproj
import math
from math import *
from sklearn.decomposition import PCA
import numpy as np
from shapely.geometry import Point, Polygon
import geopandas as gpd


class Typhoon:
    def __init__(self, TypCrd_name, TypCrd_time, TypCrd_lat, TypCrd_lon, TypCrd_pres,
                 TypCrd_wnd, TypCrd_recTime, TypCrd_grade, TypCrd_recGap):
        self.TypCrd_name = TypCrd_name
        self.TypCrd_time = TypCrd_time
        self.TypCrd_lat = TypCrd_lat
        self.TypCrd_lon = TypCrd_lon
        self.TypCrd_pres = TypCrd_pres
        self.TypCrd_wnd = TypCrd_wnd
        self.TypCrd_recTime = TypCrd_recTime
        self.TypCrd_grade = TypCrd_grade
        self.TypCrd_recGap = TypCrd_recGap

    @staticmethod
    def normalize(lst, max_val, min_val):
        print(lst, max_val, min_val)
        normalized_lst = (lst - min_val) / (max_val - min_val)

        return normalized_lst

    def check_loadPoint(self):
        for i in range(len(self.TypCrd_lat)):
            # 创建点对象
            point = Point(self.TypCrd_lon[i] / 10, self.TypCrd_lat[i] / 10)
            # 加载shp文件
            shapefile = gpd.read_file('data/GSHHS/GSHHS_l_L1.shp')
            # 判断点是否在面内
            result = shapefile.contains(point)
            if result[0]:
                #print(f"该台风登陆时间为{self.TypCrd_recTime[i]}")
                return i
            else:
                if i == len(self.TypCrd_lat) - 1:
                    # print("该台风未登陆")
                    pass
                continue
        return 0

    def calculate_shape_similarity(self, other_typhoon: 'Typhoon'):
        # 计算形状相似性
        selfCoord, otherCoord = [[], []], [[], []]
        coord_X_combine, coord_Y_combine = [], []
        SUM_X, SUM_Y = [], []
        D_ij, S_ij, C_ij = 0.0, 0.0, 0.0
        for i in range(len(self.TypCrd_lat)):
            x, y = self.geodetic_to_gauss_kruger(self.TypCrd_lat[i] / 10, self.TypCrd_lon[i] / 10)
            selfCoord[0].append(x)
            selfCoord[1].append(y)
        for j in range(len(other_typhoon.TypCrd_lat)):
            x, y = other_typhoon.geodetic_to_gauss_kruger(other_typhoon.TypCrd_lat[j] / 10,
                                                          other_typhoon.TypCrd_lon[j] / 10)
            otherCoord[0].append(x)
            otherCoord[1].append(y)

        coord_X_combine.append(selfCoord[0][-12:])
        coord_X_combine.append(otherCoord[0][-12:])
        coord_Y_combine.append(selfCoord[1][-12:])
        coord_Y_combine.append(otherCoord[1][-12:])
        if len(coord_Y_combine[0]) == len(coord_Y_combine[1]) == 12:
            for i in range(12):
                SUM_Y.append(math.fabs(coord_Y_combine[1][i] - coord_Y_combine[0][i]))  # 计算控制点纵坐标差
                SUM_X.append(math.fabs(coord_X_combine[1][i] - coord_X_combine[0][i]))  # 计算控制点纵坐标差
            for i in range(12):
                D_ij += sqrt((SUM_Y[i] ** 2 + SUM_X[i] ** 2) / 8)
            for i in range(12):
                S_ij += (sqrt(SUM_Y[i] ** 2 + SUM_X[i] ** 2) - D_ij) / 8
            C_ij = 0.7 * D_ij + 0.3 * S_ij
            return [D_ij, S_ij, C_ij]
        else:
            return [0, 0, 0]

    def calculate_impact_similarity(self, other_typhoon: 'Typhoon'):
        # 在这里编写计算影响相似性的代码
        loadtime = self.check_loadPoint()
        combine_pres, combine_wnd, combine_grade = [[], []], [[], []], [[], []]

        combine_pres[0].append(self.TypCrd_pres[loadtime:])
        combine_pres[1].append(other_typhoon.TypCrd_pres[loadtime:])

        combine_wnd[0].append(self.TypCrd_wnd[loadtime:])
        combine_wnd[1].append(other_typhoon.TypCrd_wnd[loadtime:])

        combine_grade[0].append(self.TypCrd_grade[loadtime:])
        combine_grade[1].append(other_typhoon.TypCrd_grade[loadtime:])

        similarity_score = ...

        return similarity_score

    def calculate_attributes_similarity(self, max_prwd, min_prwd, other_typhoon: 'Typhoon'):

        # 在这里编写计算属性相似性的代码
        loadtime = self.check_loadPoint()

        if len(self.TypCrd_pres[loadtime - 15:loadtime + 1]) == 16:
            arra_list = np.array(
                [self.normalize(self.TypCrd_pres[loadtime - 15:loadtime + 1], max_prwd[0], min_prwd[0]),
                 self.normalize(self.TypCrd_wnd[loadtime - 15:loadtime + 1], max_prwd[1], min_prwd[1]),
                 self.normalize(self.TypCrd_grade[loadtime - 15:loadtime + 1], 6, 0)])
            pca = PCA(n_components=3)
            # 执行PCA
            pca.fit(arra_list.T)
            # 获取降维后的数据
            reduced_data = pca.transform(arra_list.T)
            # 获取每个参数的权重
            B = pca.components_
            result = np.dot(np.array(reduced_data), np.array(B))
            row_sums = np.sum(result, axis=1, dtype=np.float64)
            print(reduced_data)
            print(row_sums)
        else:
            return 0

        similarity_score = ...

        return similarity_score

    def calculate_overall_similarity(self, other_typhoon, weights):
        # 根据权重计算综合相似性得分
        shape_similarity = self.calculate_shape_similarity(other_typhoon)
        impact_similarity = self.calculate_impact_similarity(other_typhoon)
        attributes_similarity = self.calculate_attributes_similarity(other_typhoon)

        overall_similarity = (
                weights['shape'] * shape_similarity
                + weights['impact'] * impact_similarity
                + weights['attributes'] * attributes_similarity
        )

        return overall_similarity

    @staticmethod
    def geodetic_to_gauss_kruger(latitude, longitude):
        # 定义投影坐标系，zone 参数是高斯-克吕格投影的带号，范围是1到60
        proj = pyproj.Proj(proj="utm", zone=51, ellps="WGS84")
        # 将地理坐标转换为高斯平面直角坐标
        easting, northing = proj(longitude, latitude)
        return easting, northing
