import requests

url = 'http://aicodingblock.kt.co.kr'
res = requests.get(url, verify = False)
print('test status : ', res.status_code)

