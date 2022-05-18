import pandas as pd
import re

# data[n][0] = 원래 이름
# data[n][1] = 변환된 이름
# data[n][2] = 파일 경로
def data_processing(dir_list, file_list):
    files = []
    for f_idx in range(len(file_list)):
        for idx in range(len(file_list[f_idx])):
            del_extension = extension_del_file(file_list[f_idx][idx])
            if not(del_extension == ''):
                files.append([file_list[f_idx][idx], re.sub(r"[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]", " ", del_extension),dir_list[f_idx]])
    
    df = pd.DataFrame(files)
    df.columns = ['origin', 'no-ext', 'dir']
    df.to_csv("data.csv", index=False)


def extension_del(f_list):
    extension = "jpg png docx pdf"
    extension = extension.split(' ')
    file_names = []

    for i in f_list:
        file_names.append(extension_del_file(i))

    return file_names


def extension_del_file(file):
    text = file.split('.')
    name = ''
    for j in range(len(text) - 1):
        name = name + text[j]
    return name