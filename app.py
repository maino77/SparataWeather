# flask라는 패키지에서 flask모듈을 import
# render_template()는 웹 서버에서 페이지를 랜더링
# render_template() 규칙은 templates라는 폴더 생성 후 그 안에 html 넣음
# css, js는 static이라는 폴더에 넣어줘야 flask에서 인식

from flask import Flask, request, render_template, jsonify, session, redirect, url_for


# 플라스크 객체 생성
# __name__은 현재 실행 중인 모듈의 이름
# 플라스크 인스턴스를 생성
app = Flask(__name__)

#Mongo DB연결
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

@app.route('/')
def index():
	##로그인 기능이 들어오면 수정되어야할 부분
	return render_template('index.html')

@app.route('/comment')
def comment():
	##로그인 기능이 들어오면 수정되어야할 부분
	return render_template('comment.html')


###### 코멘트 API  생성 ########
@app.route('/weather/comment', methods=['POST'])
def write_comment():
	local_receive = request.form['local_give']
	talk_receive = request.form['talk_give']
	date_receive = request.form['date_give']


	doc = {
		'local': local_receive,
		'talk': talk_receive,
		'date' : date_receive

	}
	db.album.insert_one(doc)
	return jsonify({'msg': '이 요청은 코멘트 POST'})


@app.route('/weather/comment', methods=['GET'])
def show_comment():
	comments = list(db.album.find({}, {'_id':False}))
	return jsonify({'all_comments': comments})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
