import requests

res = requests.post('http://127.0.0.1:5000/receive', json='tese')
print(res.json())
