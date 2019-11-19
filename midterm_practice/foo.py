def foo(a, b):
    try:
        print('A')
        print(len(b)/a)
        print('B')
    except ZeroDivisionError:
        print('C')
    except:
        print('D')
    else:
        print('E')
    print('F')


foo(0, 4)
foo([1, 2, 3], 3)
