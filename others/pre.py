import requests
import re
import json
import sys
import bb64
import rsa
import binascii
from bs4 import BeautifulSoup


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
		return '登录失败'
	else :
		return f.text
	#print("\n")
	#print(f.content.decode())
	#print(f.text)


	#密码base64编码
def get_pwd_rsa(n,pwd):
        #"""
        #   Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
        #    http://stuvel.eu/files/python-rsa-doc/index.html
        #"""
        #n, n parameter of RSA public key, which is published by WEIBO.COM
        #hardcoded here but you can also find it from values return from prelogin status above
        #weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'

        #e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
	weibo_rsa_e = 65537
	message = str(pwd).encode()
	
	
	rsa_n = binascii.b2a_hex(binascii.a2b_base64(n))
	print(rsa_n)
        #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
	key = rsa.PublicKey(int(rsa_n, 16), weibo_rsa_e)
		
        #get encrypted password
	encropy_pwd = rsa.encrypt(message, key)
        #trun back encrypted password binaries to hex string
	return binascii.b2a_base64(encropy_pwd) 