from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

## URL 별로 함수명이 같거나,
## route('/') 등의 주소가 같으면 안됨

#client = MongoClient('localhost', 27017)
#db = client.seoul_suljip
client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/suljip', methods=["GET"])
def get_suljip():
    # gu_receive 라는 변수에 전달받은 구, 술 종류 저장
    gu_receive = request.args.get('gu_give')
    sul_receive = request.args.get('sul_give')
    # 구, 술 종류별에 해당하는 모든 술집 목록을 불러오기
    suljip_list = list(db.suljip.find({'gu': gu_receive, 'sul': sul_receive}, {'_id': False}))
    # matjip_list 라는 키 값에 술집 목록을 담아 클라이언트단으로 반환
    return jsonify({'result': 'success', 'suljip_list': suljip_list})

@app.route('/suljip/location', methods=['POST'])
def test_origin():
    user_SX = request.form['user_longitude']
    user_SY = request.form['user_latitude']
    shop_EX = request.form['shop_longitude']
    shop_EY = request.form['shop_latitude']

    origin = {
        'SX' : user_SX,
        'SY' : user_SY,
        'EX' : shop_EX,
        'EY' : shop_EY
    }

    return jsonify({'result':origin})


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)