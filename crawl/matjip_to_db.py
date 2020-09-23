import requests
import pprint
import time
from pymongo import MongoClient

# 맛집 데이터는 seoul_suljip 이라는 데이터베이스에 저장
client = MongoClient('localhost', 27017)
db = client.seoul_suljip

# 서울시 구별로 맛집을 검색
seoul_gu = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]

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
# 구별로 검색
# 1. 와인
for gu in seoul_gu:
    # '강님구 와인', '종로구 와인 ', '용산구 와인 ' .. 반복 인코딩
    keyword_wine = f'{gu} 와인'

    # 맛집 리스트 받아오기
    suljip_list_wine = get_naver_result(keyword_wine)

    # 구별 맛집 구분선
    print("*"*80 + gu)

    for suljip_wine in suljip_list_wine:
        # 구 정보를 추가
        suljip_wine['gu'] = gu
        # 맛집을 인쇄
        pprint.pprint(suljip_wine)
        # docs에 와인맛집을 추가
        docs.append(suljip_wine)

# 2. 칵테일
for gu in seoul_gu:
    keyword_cocktail = f'{gu} 칵테일'

    # 맛집 리스트 받아오기
    suljip_list_cocktail = get_naver_result(keyword_cocktail)

    # 구별 맛집 구분선
    print("*"*80 + gu)

    for suljip_cocktail in suljip_list_cocktail:
        # 구 정보를 추가
        suljip_cocktail['gu'] = gu
        # 맛집을 인쇄
        pprint.pprint(suljip_cocktail)
        # docs에 소주맛집을 추가
        docs.append(suljip_cocktail)

# 3. 소주
for gu in seoul_gu:
    keyword_soju = f'{gu} 소주'

    # 맛집 리스트 받아오기
    suljip_list_soju = get_naver_result(keyword_soju)

    # 구별 맛집 구분선
    print("*"*80 + gu)

    for suljip_soju in suljip_list_soju:
        # 구 정보를 추가
        suljip_soju['gu'] = gu
        # 맛집을 인쇄
        pprint.pprint(suljip_soju)
        # docs에 소주맛집을 추가
        docs.append(suljip_soju)

# 4. 맥주
for gu in seoul_gu:
    keyword_beer = f'{gu} 맥주'

    # 맛집 리스트 받아오기
    suljip_list_beer = get_naver_result(keyword_beer)

    # 구별 맛집 구분선
    print("*"*80 + gu)

    for suljip_beer in suljip_list_beer:
        # 구 정보를 추가
        suljip_beer['gu'] = gu
        # 맛집을 인쇄
        pprint.pprint(suljip_beer)
        # docs에 소주맛집을 추가
        docs.append(suljip_beer)


# 맛집 정보 저장
db.suljip_wine.insert_many(docs)
db.suljip_soju.insert_many(docs)
db.suljip_beer.insert_many(docs)
db.suljip_cocktail.insert_many(docs)