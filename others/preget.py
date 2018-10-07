import requests
import re
import json
import sys
from bs4 import BeautifulSoup
 
s = requests.Session()
 
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
 
login_data = {'csrftoken': '9a0cbe42-391d-4cfc-b9a5-de01aab8e925,9a0cbe42391d4cfcb9a5de01aab8e925',
				'yhm': '201610902227',
              'mm': 'YhfMuqjjv5X8LPR3afFRQTE6BfutXpVOJtc1LX34+AmNBLQmugbTxduteWKiTa410HrNITF8EXN5HQryxhhE52sNTmi72AAUEjjYiI3Tw9s5y4VjvndVakXsijDC7XEwfFa3XAiQh7ki3oR5GLN3ttQFjXuTiOOlWG7WmpjhrxM=',
              'mm': 'YhfMuqjjv5X8LPR3afFRQTE6BfutXpVOJtc1LX34+AmNBLQmugbTxduteWKiTa410HrNITF8EXN5HQryxhhE52sNTmi72AAUEjjYiI3Tw9s5y4VjvndVakXsijDC7XEwfFa3XAiQh7ki3oR5GLN3ttQFjXuTiOOlWG7WmpjhrxM='
              }
 
url = 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html'
req = s.get(url, headers=headers)
cookies="JSESSIONID="+req.cookies['JSESSIONID']
print(cookies)           #200
content=req.content.decode()      #{"success":false,"message":"您已处于登录状态"}
	
soup = BeautifulSoup(content,"html.parser")
tokens=soup.find(id='csrftoken')
print(tokens) 


headersp = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
	'Referer': 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': cookies
} 
f = s.get('http://172.16.1.201/jwglxt/xtgl/login_getPublicKey.html', headers=headersp)
print(f.text)
sys.exit()