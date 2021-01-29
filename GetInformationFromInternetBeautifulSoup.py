import requests
from bs4 import BeautifulSoup

#CURRENTLY NOT FUNCTIONAL

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

url = "https://www.hlc.bike/ca/Catalog/Item/170786-03"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
upc = soup.select("#detailMenuContent > div.hidden-xs.top20 > div:nth-child(2) > div:nth-child(2) > div > div > div:nth-child(2)", text=True)
print(upc)
