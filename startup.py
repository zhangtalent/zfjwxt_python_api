from flask import Flask
import api
import json
from flask import request
from flask import render_template

app = Flask(__name__)




@app.route('/login', methods=['POST'])
def login():
	#获取登陆json
	result = api.login(request.form['u'],request.form['p'])	
	return result
	
@app.route('/score', methods=['POST'])
def score():
	#获取分数json
	result = api.score(request.form['year'],request.form['term'],request.form['cookie'])	
	return result	

@app.route('/detailscore', methods=['POST'])
def detailscore():
	#获取明细json
	result = api.detailscore(request.form['year'],request.form['term'],request.form['stucode'],request.form['jxb_id'],request.form['cookie'])	
	return result

@app.route('/detail', methods=['POST'])
def detail():
	#获取平时分列表json
	result = api.detaillist(request.form['year'],request.form['term'],request.form['cookie'])	
	return result

@app.route('/table', methods=['POST'])
def table():
	#获取课表列表json
	result = api.table(request.form['year'],request.form['term'],request.form['cookie'])	
	return result

@app.route('/rank', methods=['POST'])
def rank():
	#获取平排名列表json
	result = api.rank(request.form['year'],request.form['term'],request.form['stucode'],request.form['cookie'])	
	return result

@app.route('/exam', methods=['POST'])
def exam():
	#获取平排名列表json
	result = api.exam(request.form['year'],request.form['term'],request.form['cookie'])	
	return result

@app.route('/water', methods=['POST'])
def water():
	#获取电费列表json
	result = api.water(request.form['drlouming'],request.form['drceng'],request.form['zroom'],request.form['room'])	
	return result
@app.route('/sqf', methods=['POST'])
def sqf():
	#获取社区分
	result = api.sqf(request.form['xh'],request.form['mm'])	
	return result	
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)