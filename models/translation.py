import requests
from kakaotrans import Translator


def lan_analysis(f_list):
	lan_list = []
	# 카카오 번역 API이용한 언어분석
	url = "https://dapi.kakao.com/v3/translation/language/detect"
	for i in range(len(f_list)):
		queryString = {
			"query" : f_list[i]        
		}
		header = {"Authorization": "KakaoAK deeada20c669c0bc84e8e7b374315ace"}
		r = requests.get(url, headers = header, params = queryString)
		
		r_dic = r.json()
		
		language_info = r_dic["language_info"]
		language_info_first = language_info[0]
		
		lan_list.append(language_info_first["code"])

	return lan_list

def lan_translation(f_list, lan_list):
	#카카오 번역 API이용한 번역
	trans_list = []
	url = "https://dapi.kakao.com/v2/translation/translate" 
	for i in range(len(f_list)):
		queryString = {
			"query" : f_list[i],
			"src_lang" : lan_list[i],
			"target_lang" : "en"
		}
		
		header = {"Authorization": "KakaoAK deeada20c669c0bc84e8e7b374315ace"}
		
		r = requests.get(url, headers = header, params = queryString)
		r_dic = r.json()
		if 'translated_text' in r_dic:
			trans_list.append(r_dic["translated_text"][0][0])
		else:
			trans_list.append(f_list[i])
	return trans_list

def trans_test(f_list):
	translator = Translator()

	material_result_list = []

	for i in range(len(f_list)) :
		material_result_list.append(translator.translate(f_list[i], src='kr', tgt='en'))

	return(material_result_list)

'''

file_list = ['형철님_1.png','GDSC세션2인스타.png','나.좀.도와줘.docx','KakaoTalk_20220408_135926604_01.jpg','$Hola']

material_list = extension_del(file_list)

lan_list = lan_analysis(material_list)
trans_list = lan_translation(material_list, lan_list)
'''
