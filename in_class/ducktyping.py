# A "calc" is an object that knows how to perform some arbitrary
# calculation on a single input, giving a single output.
#
# It consits of one method:
#   def calculate(self,n)

class ZeroCalc:
    def calculate(self,n):
        return 0

class SquareCalc:
    def calculate(self, n):
        return n * n

class CubeCalc:
    def calculate(self,n):
        return n * n * n

class LengthCalc:
    def calculate(self,n):
        return len(n)

class MultiplyByCalc:
    def __init__(self, multiplier):
        self._multiplier = multiplier
    def calculate(self,n):
        return n * self._multiplier
    

def run_calcs(calcs: ['Calc'], start_value):
    current_value = start_value
    for calc in calcs:
        current_value = calc.calculate(current_value)

    return current_value
    
