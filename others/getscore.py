import requests
import re
import json
import sys
from bs4 import BeautifulSoup
 
s = requests.Session()
 
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded',
	'Cookie': sys.argv[4]
}
 
login_data = {'csrftoken': sys.argv[1],
				'yhm': sys.argv[2],
              'mm': sys.argv[3],
              'mm': sys.argv[3]
              }
 
url = 'http://172.16.1.201/jwglxt/xtgl/login_slogin.html'
req = s.post(url, data = login_data, headers=headers)

login_data_1 = {'xnm': '2017',
				'xqm': '',
				
              '_search': 'false',
			  'queryModel.showCount':'1000',
              'queryModel.sortOrder': 'asc'
              }
f = s.post('http://172.16.1.201/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005',data = login_data_1, headers=headers, allow_redirects=False)
print(f.status_code)
print("\n")
print(f.content.decode())
sys.exit()