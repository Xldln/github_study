import requests


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}
resp = requests.get('https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%CA%D6%D6%B8%B1%C8%CA%FD%D7%D6%B5%C4%CD%BC%C6%AC&fr=ala&ala=1&alatpl=normal&pos=0&dyTabStr=MCwzLDIsMSw2LDQsNSw3LDgsOQ%3D%3D',headers=headers)
resp.encoding='utf-8'
print(resp.text)
