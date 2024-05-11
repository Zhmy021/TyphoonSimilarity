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
    max_p = [1009, 10]
    min_p = [1008, 9]
    for i in range(len(content['Typhoon_pres'])):
        matrix_pres = np.array(content['Typhoon_pres'][i])
        matrix_wnd = np.array(content['Typhoon_wnd'][i])
        maxp = np.max(matrix_pres)
        minp = np.min(matrix_pres)
        maxwd = np.max(matrix_wnd)
        minwd = np.min(matrix_wnd)
        max_p[0] = maxp if maxp > max_p[0] else max_p[0]
        min_p[0] = minp if minp < min_p[0] else min_p[0]
        max_p[1] = maxwd if maxwd > max_p[1] else max_p[1]
        min_p[1] = minwd if minwd < max_p[1] else max_p[1]

    K = 55
    #hi = Typhoon_list[K].calculate_attributes_similarity(max_p, min_p, Typhoon_list[1])

    D, S, C = [], [], []
    tynumber = 0
    for i in tqdm(range(len(Typhoon_list)), ncols=80):
        if content['Typhoon_Name'][i] != '(nameless)' and Typhoon_list[i].check_loadPoint() != 0:
            shp = Typhoon_list[2].calculate_shape_similarity(Typhoon_list[i])
            D.append(shp[0])
            S.append(shp[1])
            C.append(shp[2])
            tynumber += 1
    print("Progress completed.")
    print(tynumber)
