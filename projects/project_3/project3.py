from call_api import api_call, json_to_dict
import datetime
import indicators
import json
import signalstrats


def run_user_interface() -> None:
    '''runs the main interface'''
    # apikey_path = input() # UNCOMMENT THIS !!!
    # comment on submit
    apikey_path = '/Users/abhinav/Documents/GitHub/ics32a_workspace/projects/project_3/apikey.txt'
    apikey = get_apikey(apikey_path)
    #symbol = input()
    symbol = 'AAPL'
    #start_date = input()
    start_date = '2018-10-01'
    #end_date = input()
    end_date = '2018-10-31'
    action = input()
    function_type, outputsize, HOST = 'TIME_SERIES_DAILY', 'full', 'https://www.alphavantage.co/'  # constants
    api_url = HOST + '/query' + '?' + 'function=' + function_type + '&' + \
        'symbol=' + symbol + '&' + 'outputsize=' + outputsize + \
        '&' + 'apikey='+apikey  # creates the url for the api call
    data_dict = {}
    data_dict = json_to_dict(api_call(api_url))
    data_key = 'Time Series (Daily)'
    date_list = list((data_dict[data_key]))
    date_list.reverse()
    while (start_date not in date_list):
        start_datetime = convert_date(start_date)
        start_datetime = start_datetime + datetime.timedelta(days=1)
        start_date = str(start_datetime)
    while (end_date not in date_list):
        end_datetime = convert_date(end_date)
        end_datetime = end_datetime - datetime.timedelta(days=1)
        end_date = str(end_datetime)
    date_list = date_list[date_list.index(
        start_date):date_list.index(end_date)+1]
    print_header(symbol, date_list, action)
    for date in date_list:
        current_dict = data_dict[data_key][date]
        ind, strat = get_indicator_and_strat(
            action, current_dict, date_list, data_key, date, data_dict)
        # print(ind.calculate())
        print_data_line(date, current_dict, ind, strat)


def print_data_line(date: str, current_dict: dict, ind: '???', strat: '???') -> None:
    '''takes the current date and the corresponding dictionary, indicator, and strategy and prints the info'''
    print(date, current_dict['1. open'], current_dict['2. high'], current_dict['3. low'],
          current_dict['4. close'], current_dict['5. volume'], ind.calculate(), strat.buy_or_not(), strat.sell_or_not(), sep='\t')


def print_header(symbol, dates, action):
    print(symbol)
    print(len(dates))
    print(action)
    print('Date', 'Open', 'High', 'Low', 'Close',
          'Volume', 'Indicator', 'Buy?', 'Sell?', sep='\t')


def get_indicator_and_strat(action, current_dict, date_list, data_key, date, data_dict):
    if action.startswith('TR'):  # TR <1.5 >0.5
        action_list = action.split()
        buy_limit = action_list[1][1:]
        sell_limit = action_list[2][1:]
        today_max = current_dict['2. high']
        today_min = current_dict['3. low']
        prev_close = 0
        if date_list.index(date) != 0:
            prev_date = date_list[date_list.index(date)-1]
            prev_close = data_dict[data_key][prev_date]['4. close']
        ind = indicators.TrueRangeIndicator(
            today_max, today_min, prev_close, buy_limit, sell_limit)
        strat = signalstrats.TrueRangeStrategy(ind, buy_limit, sell_limit)
        return ind, strat
    elif (action.startswith('MP') or action.startswith('MV')):  # MP/MV 10
        close_or_volume = '4. close'
        if (action.startswith('MV')):
            close_or_volume = '5. volume'
        action_list = action.split()
        n_days = int(action_list[1])
        n_days_closing_price_today = []
        if (date_list.index(date) >= n_days-1):
            for i in range(n_days):
                prev_date = date_list[date_list.index(date)-i]
                n_days_closing_price_today.append(float(
                    data_dict[data_key][prev_date][close_or_volume]))
        today_ind = indicators.MovingAverageIndicator(
            n_days_closing_price_today)
        n_days_closing_price_prev = []
        if (date_list.index(date) >= n_days):
            for i in range(1, n_days+1):
                prev_date = date_list[date_list.index(date)-i]
                n_days_closing_price_prev.append(float(
                    data_dict[data_key][prev_date][close_or_volume]))
        prev_ind = indicators.MovingAverageIndicator(n_days_closing_price_prev)
        today_close = current_dict[close_or_volume]
        prev_close = 0
        if date_list.index(date) != 0:
            prev_date = date_list[date_list.index(date)-1]
            prev_close = data_dict[data_key][prev_date][close_or_volume]
        strat = signalstrats.MovingAverageStrategy(
            today_ind.calculate(), prev_ind.calculate(), today_close, prev_close)
        return today_ind, strat
    elif (action.startswith('DP') or action.startswith('DV')):  # DP/DV 3 +2 -1
        close_or_volume = '4. close'
        if (action.startswith('DV')):
            close_or_volume = '5. volume'
        action_list = action.split()
        n_days = int(action_list[1])
        n_days_closing_price = []
        i = 0
        while (i < n_days+2 and date_list.index(date)-i >= 0):
            prev_date = date_list[date_list.index(date)-i]
            n_days_closing_price.append(float(
                data_dict[data_key][prev_date][close_or_volume]))
            i += 1
        n_days_closing_price.reverse()
        # print(n_days_closing_price)
        ind = indicators.DirectionalIndicator(n_days_closing_price, n_days)
        strat = signalstrats.DirectionalStrategy(
            ind.calculate(), ind._prev_calculate(), action)
        return ind, strat


def get_apikey(path: str) -> str:
    '''converts the path to the api key to the actual api key'''
    file = open(path, 'r')
    key = file.readline()
    return key[:len(key)-2]


def convert_date(str_date: str) -> datetime.date:
    '''converts a string date into a date object from the datetime module'''
    date_list = str_date.split('-')
    return datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))


if __name__ == '__main__':
    run_user_interface()
