def foo(x):
    try:
        x = len(x)
        return x
    except TypeError:
        print('A')
    else:
        print('B')
        return 2
    finally:
        print('C')


def bar(y):
    try:
        print(foo(y))
    except:
        print('D')
    print('A')


bar(1)
