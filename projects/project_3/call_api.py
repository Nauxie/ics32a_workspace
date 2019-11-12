import urllib.request
import ssl
import json


def api_call(url: str) -> str:
    '''calls the api from a given URL and returns the body (json in this case)'''
    gcontext = ssl.SSLContext()
    response = urllib.request.urlopen(url, context=gcontext)
    data = response.read()
    response.close()
    text = data.decode(encoding='utf-8')
    return text


def json_to_dict(json_data: str) -> dict:
    '''uses the json module to convert a json string into a dict'''
    data_dict = json.loads(json_data)
    return data_dict


#url = 'https://www.alphavantage.co//query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact&apikey=W7TW0AFBVH66SK7'

#print(json_to_dict(api_call(url))['Time Series (Daily)']['2019-11-08'])
