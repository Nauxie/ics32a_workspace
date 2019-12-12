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


def do_that(given: A):
    x = given.get_foo()
    x += 10
    print(20)

    #y = given.get_bar()

    y = given._bar  # y points at the same list as given._bar
    y[0] += ' there'
    print(y)
    y = ['cool']
    print(y)

    given = A(-10, ['bye'])


c = A(10, ['hello'])

do_that(c)
print(c.get_bar())
c.print()
