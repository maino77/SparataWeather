# flask라는 패키지에서 flask모듈을 import
# render_template()는 웹 서버에서 페이지를 랜더링
# render_template() 규칙은 templates라는 폴더 생성 후 그 안에 html 넣음
# css, js는 static이라는 폴더에 넣어줘야 flask에서 인식
from datetime import datetime

import requests, json
from flask import Flask, request, render_template, jsonify, redirect, url_for

# 플라스크 객체 생성
# __name__은 현재 실행 중인 모듈의 이름
# 플라스크 인스턴스를 생성
app = Flask(__name__)

# flask, pymongo, PyJWT 패키지 설치
# hashlib 별다른 설치 없이 import
# redirect, url_for 마찬가지로 설치 없이 from flask에 import

import hashlib, jwt, datetime

m = hashlib.sha256()
m.update('Life is too short'.encode('utf-8'))
m.update(', you need python.'.encode('utf-8'))


# Mongo DB연결
# 먼저 noSQL인 mogoDB를 다루기 위한 파이썬 라이브러리 Pymongo를 불러온다.
# 그 후 DB연결
# 1. MongoClient의 값으로 MongoDB 서버를 URL 파라미터로 입력
# mongodb_URL = "mongodb://local:27017/"
# client = MongoClient(mongodb_URL)

# 2. MOngoDB 서버의 호스트와 포트 각각의 값을 파라미터로 입력
# client = MongoClient(host='localhost', port=27017)
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

## mongodb 저장 경로 ##
# DB 접근 방법 2가지
# db = client.mydb 메서드 형태로 접근
# db = client['mydb'] Dictionary를 인덱싱하는 형태로 대괄호 안에 DB명 문자열을 입력
db = client.dbsparta


# [HTML]
@app.route('/')
def index():
	##로그인 기능이 들어오면 수정되어야할 부분
	return render_template('index.html')

@app.route('/comment')
def comment():
	return render_template('comment.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')


# [코멘트 API]
@app.route('/weather/comment', methods=['POST'])
def write_comment():
	local_receive = request.form['local_give']
	talk_receive = request.form['talk_give']
	date_receive = request.form['date_give']

	doc = {
		'local': local_receive,
		'talk': talk_receive,
		'date': date_receive
	}

	db.comment.insert_one(doc)
	return jsonify({'msg': '이야기를 남겨주셔서 감사합니다!'})

@app.route('/weather/comment', methods=['GET'])
def show_comment():
	comments = list(db.comment.find({}, {'_id':False}).sort('date',-1))
	return jsonify({'all_comments': comments})


# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
   id_receive = request.form['id_give']
   pw_receive = request.form['pw_give']
   nickname_receive = request.form['nickname_give']

   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

   db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

   return jsonify({'result': 'success', 'msg': '회원가입에 성공하였습니다!'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
SECRET_KEY = 'WEATHER'
@app.route('/api/login', methods=['GET','POST'])
def api_login():
    if request.method == 'GET':
        # kakao_id 받아오기, 최신꺼
        result = list(db.user.find({}).sort('_id',-1).limit(1))
        result = result[0]
        print(result)
        # db.comment.find({}, {'_id':False}).sort('date',-1)).limite()
        if result is not None:
            # JWT 토큰에는, payload와 시크릿키가 필요합니다.
            # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
            # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
            # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
            id = result['id']
            payload = {
                'id': id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)  # 언제까지 유효한지
            }

            # jwt를 암호화
            # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            # token을 줍니다.
            #return jsonify({'result': 'success', 'token': token})
            json_data ={'token' : token }
            return render_template('index_ok.html', json_data_client =json_data)
            # 찾지 못하면
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

    else :
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        print(type(id_receive))
        # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

        # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
        result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
        if result is not None:
            # JWT 토큰에는, payload와 시크릿키가 필요합니다.
            # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
            # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
            # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
            payload = {
                'id': id_receive,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)  # 언제까지 유효한지
            }

            # jwt를 암호화
            # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            # token을 줍니다.
            return jsonify({'result': 'success', 'token': token})
            # 찾지 못하면
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

   # 찾으면 JWT 토큰을 만들어 발급합니다.



@app.route('/aouth/callback', methods=['GET'])
def aouth():
    # code는 index.html에 카카오 버튼 url을 보면 알 수 있습니다. 버튼 url에 만든사람 인증id, return uri이 명시되어 있습니다.
    # 사용자 로그인에 성공하면 로그인 한 사람의 코드를 발급해줍니다.
    code = request.args.get('code')

    # 그 코드를 이용해 서버에 토큰을 요청해야 합니다. 아래는 POST 요청을 위한 header와 body입니다.
    url = 'https://kauth.kakao.com/oauth/token'
    client_id = '1a69011965359e16785c0d5069275e4f'
    redirect_uri = 'http://localhost:5001/aouth/callback'  # APP에서 등록한 redirect_url
    my_code = code
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code': my_code,
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    # rint(tokens["access_token"])

    info_url = 'https://kapi.kakao.com/v2/user/me'
    info_headers = {
        'Authorization': 'Bearer ' + tokens['access_token'],
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    info_response = requests.post(url=info_url, headers=info_headers)
    infos = info_response.json()

    # kakao_id = str(infos['email'])

    email = infos['kakao_account']['email'].split('@')[0]
    print(type(email))
    kakao_name = infos['properties']['nickname']

    exist = bool(db.user.find_one({'id': email}))
    print(exist)
    if exist is False:
        doc = {
            'id': email,
            'nick': kakao_name
        }
        db.user.insert_one(doc)
    result = db.user.find_one({'id': email})
    print(result)
    return render_template('index_ok.html', nickname=result["nick"])
    #return redirect(url_for("api_login"))



# [회원전용]
@app.route('/index_ok')
def index_ok():

   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.user.find_one({"id": payload['id']})
      return render_template('index_ok.html', nickname=user_info["nick"])
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

'''
def get_jwt_token(user_id):
    payload = {
        'id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # 토큰을 발급하고

    # response = make_response(redirect(url_for('main_page')))  # 쿠키를 저장해줄 페이지 지정(?)
    # response.set_cookie(TOKEN_NAME, token)  # 메인페이지 기준으로 쿠키 설정(?)
    return token
'''

@app.route('/comment_ok')
def comment_ok():
   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.user.find_one({"id": payload['id']})
      return render_template('comment_ok.html', nickname=user_info["nick"])
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
