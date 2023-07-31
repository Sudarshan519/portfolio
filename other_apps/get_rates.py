import requests
import datetime
from threading import Timer
import json
def get_rates(): 
    params = { "format": "json"}#"words": 10, "paragraphs": 1,
    to=datetime.datetime.now().strftime('%Y-%m-%d')
    url=f'https://www.nrb.org.np/api/forex/v1/rates?page=1&per_page=100&from={to}&to={to}'
    r =  requests.get(url) 
    # print(r.json()['data']['payload'])
    return r.json()['data']['payload'][0]