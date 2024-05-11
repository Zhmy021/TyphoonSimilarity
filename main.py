import ShapeSimilarity.readtxtfile as rd
from Typhoon import Typhoon
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    data = rd.loadfile('C:/Users/zmyzq/Desktop/台风/CMABSTdata')
    content = data.readTxtFile()
    Typhoon_list = []

    for i in range(len(content['Typhoon_Name'])):
        typhoon = Typhoon(content['Typhoon_Name'][i], content['Typhoon_time'][i], content['Typhoon_lat'][i],
                          content['Typhoon_lon'][i], content['Typhoon_pres'][i], content['Typhoon_wnd'][i],
                          content['Typhoon_record_time'][i], content['Typhoon_grade'][i], content['Typhoon_recGap'][i])
        Typhoon_list.append(typhoon)
    max_p = 1009
    min_p = 1008
    for i in range(len(content['Typhoon_pres'])):
        matrix_pres = np.array(i)
        max_ = np.max(matrix_pres)
        min_ = np.min(matrix_pres)
        if max_ > max_p:
            max_p = max_
        if min_ < min_p:
            min_p = min_

    K = 2000
    hi = Typhoon_list[K].calculate_attributes_similarity(max_p, min_p, Typhoon_list[1])

    D, S, C = [], [], []
    for i in tqdm(range(len(Typhoon_list)), ncols=80):
        shp = Typhoon_list[2].calculate_shape_similarity(Typhoon_list[i])
        D.append(shp[0])
        S.append(shp[1])
        C.append(shp[2])
    print("Progress completed.")
