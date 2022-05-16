import requests
import json
from kakaotrans import Translator

file_list = ['형철님_1.png','GDSC세션2인스타.png','나.좀.도와줘.docx','KakaoTalk_20220408_135926604_01.jpg','$Hola']
file_list2 = [i for i in enumerate(file_list)]

material_list = []
material_list2 = []
material_list3 = file_list

lan_list = []
trans_list = []

extension = "jpg png docx pdf"
#사용할거면 확장자 추가해야함
extension = extension.split(' ')

for i in file_list:
    text = i.split('.')
    material = ''
    for j in text:
        if j not in extension:
            material = material + j
    material_list.append(material)
# 적당히 만들어본 전처리1

for i in file_list2:
    text = i[1].split('.')
    material = ''
    for j in text:
        if j not in extension:
            material = material + j
    material_list2.append((i[0],material))
# 적당히 만들어본 전처리2

print(file_list)
print(material_list)
print(file_list2)
print(material_list2)
print(material_list3)


# 카카오 번역 API이용한 언어분석
url = "https://dapi.kakao.com/v3/translation/language/detect"
for i in range(len(material_list)):
    queryString = {
        "query" : material_list[i]        
    }
    header = {"Authorization": "KakaoAK deeada20c669c0bc84e8e7b374315ace"}
    r = requests.get(url, headers = header, params = queryString)
    
    r_dic = r.json()
    
    language_info = r_dic["language_info"]
    language_info_first = language_info[0]
    
    lan_list.append(language_info_first["code"])

print(material_list)
print(lan_list)

#카카오 번역 API이용한 번역
url = "https://dapi.kakao.com/v2/translation/translate" 
for i in range(len(material_list)):
    queryString = {
        "query" : material_list[i],
        "src_lang" : lan_list[i],
        #"src_lang" : "kr", #단어 선택 X
        "target_lang" : "en"
    }
    
    header = {"Authorization": "KakaoAK deeada20c669c0bc84e8e7b374315ace"}
    
    r = requests.get(url, headers = header, params = queryString)
    r_dic = r.json()
    trans_list.append(r_dic["translated_text"][0][0])

'''
url = "https://dapi.kakao.com/v2/translation/translate" 
for i in range(len(material_list2)):
    queryString = {
        "query" : material_list2[i][1],
        #"src_lang" : lan_list[i],
        "src_lang" : "kr", #단어 선택 X
        "target_lang" : "en"
    }
    
    header = {"Authorization": "KakaoAK deeada20c669c0bc84e8e7b374315ace"}
    
    r = requests.get(url, headers = header, params = queryString)
    r_dic = r.json()
    trans_list.append((material_list2[i][0],r_dic["translated_text"][0][0]))
'''
    
print(trans_list)

#API가 아닌 그냥 번역 프로그램
from kakaotrans import Translator

translator = Translator()

material_result_list = []

for i in range(len(material_list)) :
   material_result_list.append(translator.translate(material_list[i], src=lan_list[i], tgt='en'))

print(material_result_list)
