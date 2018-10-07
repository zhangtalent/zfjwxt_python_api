import requests
import re
import json
import sys
import rsa
import base64
import binascii
from bs4 import BeautifulSoup
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5



#登陆
def login(yhm,mm):
		
	s = requests.Session()
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	}
 
	#获取cookies and tokens
	url = 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html'
	req = s.get(url, headers=headers)
	cookies="JSESSIONID="+req.cookies['JSESSIONID']
	#print(cookies)           #200
	content=req.content.decode()      #{"success":false,"message":"您已处于登录状态"}
	#print(content)	
	soup = BeautifulSoup(content,"html.parser")
	
	tokens=soup.find(id='csrftoken').get("value")
	#print(tokens) 


	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
		'Cookie': cookies
	} 
	#获取modulus,
	f = s.get('http://172.16.1.201/jwglxt/xtgl/login_getPublicKey.html', headers=headersp)
	key = f.text

	data2 = json.loads(key)
	mkey = data2['modulus']
 
	#print (mkey)

	#密码编码
	hmm = get_pwd_rsa(mkey,mm)
	#print(hmm)
	login_data = {'csrftoken': tokens,
				'yhm': yhm,
				'mm': hmm,
				'mm': hmm
              }
 
	url = 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html'
	req = s.post(url, data = login_data, headers=headersp)
	#print(req.content.decode())
	login_data_1 = {'xnm': '2017',
				'xqm': '12',
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc'
              }
	f = s.post('http://172.16.1.201/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query',data = login_data_1, headers=headersp
				, allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return '{"result":"ok","cookie":"'+cookies+'"}'

		
#获取成绩
def score(year,term,cookie):
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
		'Cookie': cookie
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc'
              }
	f = s.post('http://172.16.1.201/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query',data = data_1, headers=headersp
				, allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text

#获取考试信息
def exam(year,term,cookie):
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
		'Cookie': cookie
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc'
              }
	f = s.post('http://172.16.1.201/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query',data = data_1, headers=headersp
				, allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text


#获取课表信息
def table(year,term,cookie):
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
		'Cookie': cookie
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc'
              }
	f = s.post('http://172.16.1.201/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151',data = data_1, headers=headersp
				, allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text	

#获取排名信息
def rank(year,term,stucode,cookie):
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
		'Cookie': cookie
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc',
				'xh':stucode,
				'tjlx': '1'
              }
	f = s.post('http://172.16.1.201/jwglxt/cjpmtj/cjpmtj_cxCjpmtjIndex.html?doType=query&gnmkdm=N305005',data = data_1, headers=headersp
				, allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text

#获取平时分列表
def detaillist(year,term,cookie):
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
		'Cookie': cookie
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc'
              }
	f = s.post('http://172.16.1.201/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005',data = data_1, headers=headersp
				, allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text

#获取平时分
def detailscore(year,term,stucode,jxb_id,cookie):
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
		'Cookie': cookie
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc',
				'xh_id':stucode,
				'jxb_id': jxb_id
              }
	f = s.post('http://172.16.1.201/jwglxt/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305005&su='+stucode,data = data_1, headers=headersp
				, allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text
#查询社区分(登陆)
def getverify():
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html'
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc',
				'xh_id':stucode,
				'jxb_id': jxb_id
              }
	f = s.get('http://172.16.1.201/jwglxt/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305005&su=', allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text
#查询社区分(登陆)
def sqflogin():
	s = requests.Session()
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html'
	}
	#post的form数据
	data_1 = {'xnm': year,
				'xqm': term,
				'_search': 'false',
				'queryModel.showCount':'1000',
				'queryModel.sortOrder': 'asc',
				'xh_id':stucode,
				'jxb_id': jxb_id
              }
	f = s.get('http://172.16.1.201/jwglxt/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305005&su=', allow_redirects=False)
	code = f.status_code
	if code==302:
		return '{"result":"fail"}'
	else :
		return f.text		
#获取处风大的水电费
def water(drlouming,drceng,zroom,room):
	s = requests.Session()
	cookie = ''
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.148.20/cx/default.aspx'
		#'Cookie': cookie
	}
	
	f = s.get('http://172.16.148.20/cx/default.aspx')
	#cookies="JSESSIONID="+f.cookies['JSESSIONID']
	
	sss='/wEPDwUKLTQ0MDY2MDE3Ng9kFgICAQ9kFgQCAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQhST09NTkFNRR4ORGF0YVZhbHVlRmllbGQFBnJvb21kbR4LXyFEYXRhQm91bmRnZBAVDgbmpbzmoIsP5Y2X5Yy655S355Sf5qW8D+WNl+WMuuWls+eUn+alvAnnrqHpmaIxMCMJ566h6ZmiMTEjCuWMu+WtpumZokEK5Yy75a2m6ZmiQwrljLvlrabpmaJECuWMu+WtpumZokUJ5a2m5Zut5LicCeWtpuWbreilvwnpm6rmtKXmpbwJ5LiJ6Lev5qW8CeaWsOWFrOWvkxUOAAIxMQIxMgIyMAIyMQIzMQIzMgIzMwIzNAIzNQIzNgIzOQI0MAI0MRQrAw5nZ2dnZ2dnZ2dnZ2dnZxYBZmQCAw8QZGQWAWZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYEBQRidXlSBQV1c2VkUgUMSW1hZ2VCdXR0b24xBQxJbWFnZUJ1dHRvbjIR+XwstJ/BtkF6xbJvjrNWOFOjqNn1n5o3P3Ks5RHYYA=='
	#post的form数据
	data_1 = {'__EVENTTARGET': 'drlouming',
				'__VIEWSTATE': sss,
				'__VIEWSTATEGENERATOR': '50D05110',
				'drlouming':drlouming
              }
	f = s.post('http://172.16.148.20/cx/default.aspx',data = data_1, headers=headersp
				, allow_redirects=False)
	s = requests.Session()
	content=f.text

	soup = BeautifulSoup(content,"html.parser")
	
	viewstate1 = soup.find(id='__VIEWSTATE').get("value")

	#post的form数据
	data_2 = {'__EVENTTARGET': 'drceng',
				'__VIEWSTATE': viewstate1,
				'__VIEWSTATEGENERATOR': '50D05110',
				'drceng':drlouming+drceng
              }
	f = s.post('http://172.16.148.20/cx/default.aspx',data = data_2, headers=headersp
				, allow_redirects=False)
	
	content=f.text

	soup = BeautifulSoup(content,"html.parser")
	
	viewstate2 = soup.find(id='__VIEWSTATE').get("value")

	
	
	
	
	#post的form数据
	data_3 = {'__EVENTTARGET': '',
				'__LASTFOCUS': '',
				'__VIEWSTATE': viewstate2,
				'__VIEWSTATEGENERATOR': '50D05110',
				'drlouming':drlouming,
				'__EVENTARGUMENT': '',
				'drfangjian': drlouming+drceng+zroom[(len(zroom)-2):len(zroom)],
				'drceng':drlouming+drceng,
				'ImageButton1.y': '12',
				'ImageButton1.x': '65',
				'radio':'usedR'
              }
	#s = requests.Session()			
	f = s.post('http://172.16.148.20/cx/default.aspx',data = data_3, allow_redirects=False)
	cookie="ASP.NET_SessionId="+f.cookies['ASP.NET_SessionId']
	
	
	#post的form数据
	#模拟头部信息
	headersp = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.148.20/cx/default.aspx',
		'Cookie': cookie
	}
		
	f = s.get('http://172.16.148.20/cx/usedRecord.aspx',headers=headersp)
	
	content=f.text

	soup = BeautifulSoup(content,"html.parser")
	
	data = soup.h6.text
	
	VIEWSTATE = soup.find(id='__VIEWSTATE').get("value")
	VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR').get("value")
	EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get("value")
	#post的form数据
	data_4 = {'btnser': '查询',
				'txtend': '2019-12-31',
				'txtstart': '2018-05-31',
				'__VIEWSTATE': VIEWSTATE,
				'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR,
				'__EVENTVALIDATION': EVENTVALIDATION
              }
	#s = requests.Session()			
	f = s.post('http://172.16.148.20/cx/usedRecord.aspx',data = data_4, allow_redirects=False)
	
	content=f.text

	soup = BeautifulSoup(content,"html.parser")
	
	 
	
	data += soup.table.text
	
	return data;
		
#密码base64编码
def get_pwd_rsa(n,pwd):

	rsa_e = 65537
	message = str(pwd).encode()
	rsa_n = binascii.b2a_hex(binascii.a2b_base64(n))
	key = rsa.PublicKey(int(rsa_n, 16), rsa_e)
	encropy_pwd = rsa.encrypt(message, key)

	return binascii.b2a_base64(encropy_pwd) 

	

	
def sqf(username,password):

	#获取cookie,事实上不需要的，cookie似乎是永久存在的
	s = requests.Session()
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	}
	url = 'http://172.16.1.209/PtuXG/Sys/UserLogin.aspx'
	
	req = s.get(url, headers=headers)
	content = req.text
	cookie="ASP.NET_SessionId="+req.cookies['ASP.NET_SessionId']
	#print(cookies)           #打印cookie
	soup = BeautifulSoup(content,"html.parser")
	__LASTFOCUS = soup.find(id='__LASTFOCUS').get("value")
	__VIEWSTATE = soup.find(id='__VIEWSTATE').get("value")
	__VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR').get("value")
	__EVENTTARGET = soup.find(id='__EVENTTARGET').get("value")
	__EVENTARGUMENT = soup.find(id='__EVENTARGUMENT').get("value")
	__EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get("value")
	pubKey = soup.find(id='pubKey').get("value")
	EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get("value")


	#post的form数据
	data_3 = {'__LASTFOCUS': '',
				'__VIEWSTATE': __VIEWSTATE,
				'__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
				'__EVENTTARGET': '',
				'__EVENTARGUMENT':'',
				'__EVENTVALIDATION': __EVENTVALIDATION,
				'UserName': username,
				'UName':encrypt_sqf(pubKey,username),
				'Password': 'JsCMqs',
				'pwd': encrypt_sqf(pubKey,password),
				'pubKey':pubKey,
				'codeInput':'0000',
				'queryBtn':("登          录")
              }
	#模拟头部信息
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.209/PtuXG/Sys/UserLogin.aspx',
		'Cookie': cookie
	}		  
	s = requests.Session()			
	f = s.post('http://172.16.1.209/PtuXG/Sys/UserLogin.aspx',data = data_3,headers=headers, allow_redirects=False)
	if("CenterSoft" not in f.cookies.get_dict()):
		return '{"result":"fail"}'
	
		
	cookiecs=";CenterSoft="+f.cookies['CenterSoft']
	#cookie="ASP.NET_SessionId="+f.cookies['ASP.NET_SessionId']	
	#模拟头部信息
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Referer': 'http://172.16.1.209/PtuXG/Sys/UserLogin.aspx',
		'Cookie': cookie+cookiecs
	}
	#获取分数最新的
	b = s.get('http://172.16.1.209/PtuXG/Sys/SystemForm/Gardens/StuMyCivilization.aspx')
	soup = BeautifulSoup(b.text,"html.parser")
	si = 0
	des = ''
	for string in soup.find(id='GridView1').stripped_strings:
		if(si>=10):
			des += string.replace("\n","")
			des += "<br>"
		si += 1	
	#输出加减分明细，bs框架不太会用只能text了
	f = s.get('http://172.16.1.209/PtuXG/Sys/SystemForm/Gardens/Civilization_Edit.aspx?From=Stu&StudentId='+username+'&BeginYear=2018&Point=100.00',headers=headers, allow_redirects=False)
	soup = BeautifulSoup(f.text,"html.parser")
	si = 0
	des += "<br>"
	for string in soup.find(id='GridView1').stripped_strings:
		if(si>=8):
			des += string.replace("\n","")
			des += "<br>"
		si += 1	
	
	return '{"result":"ok","data":"'+des+'"}'
#	
def encrypt_sqf(pkey,str):
    # 加载公钥
	privateKey = pkey 
	
	private_keyBytes = base64.b64decode(privateKey)
	priKey = RSA.importKey(private_keyBytes)

	signer = PKCS1_v1_5.new(priKey)
	signature = base64.b64encode(signer.encrypt(str.encode("utf-8")))
	return signature
