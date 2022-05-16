import csv
import pandas as pd
import re

# data[n][0] = 원래 이름
# data[n][1] = 변환된 이름
def data_processing(file_list):
    for f_idx in range(len(file_list)):
        file_list[f_idx] = [file_list[f_idx], re.sub(r"[^a-zA-Z0-9 ]", "", file_list[f_idx])]
    
    df = pd.DataFrame(file_list)
    df.to_csv("data.csv", index=False)