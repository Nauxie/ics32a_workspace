import datetime
from statistics import mean


class TrueRangeIndicator:
    def __init__(self, tmax, tmin, yclose, buy, sell):
        self.max = float(tmax)
        self.min = float(tmin)
        self.close = float(yclose)
        self.buy = buy
        self.sell = sell

    def calculate(self):
        if (self.close == 0):
            return ''
        else:
            return "{0:.4f}".format((((max(self.max, self.min, self.close) - min(self.max, self.min, self.close)) / (self.close)) * 100))


class MovingAverageIndicator:
    def __init__(self, closing_list):
        self.closing_list = closing_list

    def calculate(self):
        if (len(self.closing_list) == 0):
            return ''
        else:
            return "{0:.4f}".format(mean(self.closing_list))


class DirectionalIndicator:
    def __init__(self, closes_list, n_days):
        if (len(closes_list) <= n_days+1):
            self.closes_list = closes_list
        else:
            self.closes_list = closes_list[1:]

        self.closes_list_prev = closes_list[:-1]
        self.n_days = n_days
        #print(self.closes_list, self.closes_list_prev)

    def calculate(self):
        directional_counter = 0
        for i in range(0, len(self.closes_list)-1):
            if (self.closes_list[i+1] > self.closes_list[i]):
                directional_counter += 1
            elif (self.closes_list[i+1] < self.closes_list[i]):
                directional_counter -= 1
        if (directional_counter == 0):
            return ' 0'
        else:
            return ("%+d" % directional_counter)

    def _prev_calculate(self):
        directional_counter = 0
        for i in range(0, len(self.closes_list_prev)-1):
            if (self.closes_list_prev[i+1] > self.closes_list_prev[i]):
                directional_counter += 1
            elif (self.closes_list_prev[i+1] < self.closes_list_prev[i]):
                directional_counter -= 1
        if (directional_counter == 0):
            return directional_counter
        else:
            return ("%+d" % directional_counter)
