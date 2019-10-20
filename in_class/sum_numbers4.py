def sum_numbers(numlist: 'nested list of integers') -> int:
    total = 0
    for element in numlist:
        if type(element) == list:
            total += sum_numbers(element)
        else:
            total += element
    return total


assert(sum_numbers([1,2,3,4,5]) == 15)
assert(sum_numbers([[[[1,2,[1,2]]]],122])) == 128