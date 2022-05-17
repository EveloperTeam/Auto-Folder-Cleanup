import csv
import pandas as pd
import re
from models.translation import extension_del, extension_del_file

# data[n][0] = 원래 이름
# data[n][1] = 변환된 이름
# data[n][2] = 파일 경로
def data_processing(dir_list, file_list):
    files = []
    for f_idx in range(len(file_list)):
        for idx in range(len(file_list[f_idx])):
            files.append([file_list[f_idx][idx], re.sub(r"[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]", " ", extension_del_file(file_list[f_idx][idx])),dir_list[f_idx]])
    
    df = pd.DataFrame(files)
    df.columns = ['Before', 'After', 'Dir']
    df.to_csv("data.csv", index=False)