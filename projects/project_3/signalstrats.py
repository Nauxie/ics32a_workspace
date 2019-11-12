class TrueRangeStrategy:
    def __init__(self, indicator, buy_percent, sell_percent):
        self.indicator = indicator
        self.buy_percent = buy_percent
        self.sell_percent = sell_percent

    def buy_or_not(self):
        if (self.indicator.calculate() != ''):
            if (self.indicator.calculate() < self.buy_percent):
                return 'BUY'
            else:
                return ''
        else:
            return ''

    def sell_or_not(self):
        if (self.indicator.calculate() > self.sell_percent):
            return 'SELL'
        else:
            return ''


class MovingAverageStrategy:
    def __init__(self, today_ind, prev_ind, today_close, prev_close):
        self.today_ind = today_ind
        self.prev_ind = prev_ind
        self.today_close = today_close
        self.prev_close = prev_close

    def buy_or_not(self):
        if (self.today_ind != '' and self.prev_ind != ''):
            if (self.prev_close < self.prev_ind and self.today_close > self.today_ind):
                return 'BUY'
            else:
                return ''
        else:
            return ''

    def sell_or_not(self):
        if (self.today_ind != '' and self.prev_ind != ''):
            if (self.prev_close > self.prev_ind and self.today_close < self.today_ind):
                return 'SELL'
            else:
                return ''
        else:
            return ''


class DirectionalStrategy:
    def __init__(self, indicator_value, indicator_value_prev, action_string):  # DP 3 +2 -1
        self.indicator_value = int(indicator_value)
        self.indicator_value_prev = int(indicator_value_prev)
        action_split = action_string.split()
        self.buy_threshhold = int(action_split[2])
        self.sell_threshhold = int(action_split[3])

    def buy_or_not(self):
        if (self.indicator_value > self.buy_threshhold and self.indicator_value_prev <= self.buy_threshhold):
            return 'BUY'
        else:
            return ''

    def sell_or_not(self):
        if (self.indicator_value < self.sell_threshhold and self.indicator_value_prev >= self.sell_threshhold):
            return 'SELL'
        else:
            return ''
