import pyproj
import math
from math import *


class Typhoon:
    def __init__(self, TypCrd_name, TypCrd_time, TypCrd_lat, TypCrd_lon, TypCrd_pres, TypCrd_wnd, TypCrd_recTime):
        self.TypCrd_name = TypCrd_name
        self.TypCrd_time = TypCrd_time
        self.TypCrd_lat = TypCrd_lat
        self.TypCrd_lon = TypCrd_lon
        self.TypCrd_pres = TypCrd_pres
        self.TypCrd_wnd = TypCrd_wnd
        self.TypCrd_recTime = TypCrd_recTime

    def check_loadPoint(self):
        from shapely.geometry import Point, Polygon
        import geopandas as gpd

        for i in range(len(self.TypCrd_lat)):
            # 创建点对象
            point = Point(self.TypCrd_lon[i] / 10, self.TypCrd_lat[i] / 10)
            # 加载shp文件
            shapefile = gpd.read_file('data/GSHHS/GSHHS_l_L1.shp')
            # 判断点是否在面内
            result = shapefile.contains(point)
            if result[0]:
                return i, self.TypCrd_recTime[i]
            else:
                continue

        return None

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

        coord_X_combine.append(selfCoord[0][-8:])
        coord_X_combine.append(otherCoord[0][-8:])
        coord_Y_combine.append(selfCoord[1][-8:])
        coord_Y_combine.append(otherCoord[1][-8:])
        if len(coord_Y_combine[0]) == 8 and len(coord_Y_combine[1]) == 8:
            for i in range(8):
                SUM_Y.append(math.fabs(coord_Y_combine[1][i] - coord_Y_combine[0][i]))  # 计算控制点纵坐标差
                SUM_X.append(math.fabs(coord_X_combine[1][i] - coord_X_combine[0][i]))  # 计算控制点纵坐标差
            for i in range(8):
                D_ij += sqrt((SUM_Y[i] ** 2 + SUM_X[i] ** 2) / 8)
            for i in range(8):
                S_ij += (sqrt(SUM_Y[i] ** 2 + SUM_X[i] ** 2) - D_ij) / 8
            C_ij = 0.7 * D_ij + 0.3 * S_ij
            return [D_ij, S_ij, C_ij]
        else:
            return [0, 0, 0]

    def calculate_impact_similarity(self, other_typhoon):
        # 在这里编写计算影响相似性的代码
        similarity_score = ...

        return similarity_score

    def calculate_attributes_similarity(self, other_typhoon):
        # 在这里编写计算属性相似性的代码
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
