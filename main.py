import ShapeSimilarity.readtxtfile as rd
from Typhoon import Typhoon
import time

from tqdm import tqdm
import time


if __name__ == '__main__':
    data = rd.loadfile('C:/Users/zmyzq/Desktop/台风/CMABSTdata')
    content = data.readTxtFile()
    Typhoon_list = []

    for i in range(len(content['Typhoon_Name'])):
        tyhoon = Typhoon(content['Typhoon_Name'][i], content['Typhoon_time'][i], content['Typhoon_lat'][i],
                         content['Typhoon_lon'][i], content['Typhoon_pres'][i], content['Typhoon_wnd'][i])
        Typhoon_list.append(tyhoon)
    D, S, C = [], [], []
    for i in tqdm(range(len(Typhoon_list)), ncols=80):
        shp = Typhoon_list[2].calculate_shape_similarity(Typhoon_list[i])
        D.append(shp[0])
        S.append(shp[1])
        C.append(shp[2])
    print("Progress completed.")