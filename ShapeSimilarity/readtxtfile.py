import os
import pandas as pd
import pyproj


class loadfile:
    def __init__(self, dataFolder):
        self.dataFolder = dataFolder

    @staticmethod
    def remove_spaces_from_list(input_list):
        #
        result_list = []
        for item in input_list:
            if isinstance(item, str):
                cleaned_item = item.replace(" ", "")
                result_list.append(cleaned_item)
            else:
                result_list.append(item)
        return result_list

    def readTxtFile(self):
        file_name = os.listdir(self.dataFolder)
        all_lines = []

        for i in file_name:
            ph = os.path.join(self.dataFolder, i)
            source = open(ph, 'r')
            content = source.readlines()
            all_lines = all_lines + content

        dataset = []
        for line in all_lines:
            line = line.strip().split('\t')
            dataset.append(line)
        df = pd.DataFrame(dataset)

        Typhoon_Name, Typhoon_record_num, Typhoon_record_time = [], [], []
        Typhoon_grade, Typhoon_coord_lat, Typhoon_coord_long = [], [], []
        Typhoon_pres, Typhoon_wnd = [], []

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
        Typhoon_Name = self.remove_spaces_from_list(Typhoon_Name)
        Typhoon_record_time = [i[0] for i in Typhoon_record_time]

        return {"Typhoon_Name": Typhoon_Name,
                "Typhoon_time": Typhoon_record_time,
                "Typhoon_lat": Typhoon_coord_lat,
                "Typhoon_lon": Typhoon_coord_long,
                "Typhoon_pres": Typhoon_pres,
                "Typhoon_wnd": Typhoon_wnd,
                "Typhoon_grade": Typhoon_grade,
                "Typhoon_record_num": Typhoon_record_num}

