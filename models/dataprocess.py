import csv
import pandas as pd
import re

def data_processing(file_list):
    for f_idx in range(len(file_list)):
        file_list[f_idx] = re.sub(r"[^a-zA-Z0-9 ]", "", file_list[f_idx])
    
    df = pd.DataFrame(file_list)
    df.to_csv("data.csv", index=False)