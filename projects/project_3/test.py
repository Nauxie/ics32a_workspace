# import call_api.api_call
import json
import datetime

# api_url = 'https://www.alphavantage.co//query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact&apikey=W7TW0AFBVH66SK7'
# data = api_call(api_url)
# print(data)

data_dict = {}


def convert_date(str_date: str) -> datetime.date:
    date_list = str_date.split('-')
    return datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))


with open('msft_compact.json', 'r') as f:
    data_dict = json.load(f)


start_date = '2019-11-02'
end_date = '2019-11-11'
date_list = list((data_dict['Time Series (Daily)']))
date_list.reverse()
while (start_date not in date_list):
    start_datetime = convert_date(start_date)
    start_datetime = start_datetime + datetime.timedelta(days=1)
    start_date = str(start_datetime)
while (end_date not in date_list):
    end_datetime = convert_date(end_date)
    end_datetime = end_datetime - datetime.timedelta(days=1)
    end_date = str(end_datetime)
print(start_date, end_date)
date_list = date_list[date_list.index(start_date):date_list.index(end_date)+1]
for date in date_list:
    current_dict = data_dict['Time Series (Daily)'][date]
    print(date, current_dict['1. open'], current_dict['2. high'], current_dict['3. low'],
          current_dict['4. close'], current_dict['5. volume'], sep='\t')
