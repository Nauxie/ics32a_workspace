val = int(input())
two_plus,two_line,three_plus = '+-+','| |','+-+-+'

def diagonal_block(n):
    print(two_plus)
    print(two_line)
    if(n==1): 
        print(two_plus)
    else:
        for i in range(n-1):
            print(((i)*2 * ' ') + three_plus)
            print(((i+1)*2 * ' ') + two_line)
        print((n-1)*2 *' ' + two_plus)

diagonal_block(val)



