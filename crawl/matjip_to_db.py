import requests
import pprint
import time
from pymongo import MongoClient

# 술집 데이터는 seoul_suljip 이라는 데이터베이스에 저장
#client = MongoClient('localhost', 27017)
#db = client.seoul_suljip

client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbsparta


# 서울시 구별로 술집을 검색
seoul_gu = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]
seoul_sul = ["와인", "칵테일", "소주", "맥주"]
# 네이버 검색 API 아이디와 시크릿 키
client_id = "uQBabSo2SlUiRpaco6iL"
client_secret = "HtrjQr6HZQ"

# 검색어를 전달하면 결과를 반환하는 함수
def get_naver_result(keyword):
    time.sleep(0.1)
    # url에 전달받은 검색어 삽입
    api_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=10&start=1&sort=random"
    # 아이디와 시크릿 키를 부가 정보로 header에 실어 보내기
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    # 검색 결과를 data에 저장
    data = requests.get(api_url, headers=headers)
    # 받아온 JSON 결과를 딕셔너리로 변환
    data = data.json()
    return data['items']


# 저장할 전체 맛집 목록
docs = []

#술 종류별로 검색
for sul in seoul_sul:
    # 술집안에서 구별로 또 검색
    for gu in seoul_gu:
        keyword = f'{gu} {sul}'
        # 술집 리스트 받아오기
        suljip_list = get_naver_result(keyword)

        # 구별 술집 구분선
        print("*"*80 + gu + sul)

        # 구, 술종류 정보를 추가
        for suljip in suljip_list:
            suljip['gu'] = gu
            suljip['sul'] = sul

            #술집 프린트
            pprint.pprint(suljip)

            # docs에 술집들 추가
            docs.append(suljip)

# 술집 정보 저장
db.suljip.insert_many(docs)
