import requests

url = 'http://192.168.1.{id}:3333'

for idx in range(1, 24):
    print(idx)
    with open('node{id:02}.txt'.format(id=idx), 'wb') as f:
        res = requests.get(url.format(id=idx+10))
        f.write(res.content)
