class A:
    def __init__(self, a: int, b: [str]):
        self._foo = a
        self._bar = b

    def get_foo(self):
        return self._foo

    def get_bar(self):
        return self._bar

    def print(self):
        print(self._foo, self._bar)

    def string_change(self):
        x = self.get_bar()  # x = given._bar
        x = 'hello'


test = A(100, 'string')
print(test._bar)
test.string_change()
print(test._bar)
