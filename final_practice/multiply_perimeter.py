def multiply_perimeter(L, multiplier):
    for i in range(len(L)):
        for j in range(len(L[i])):
            if (i == 0 or j == 0 or i == len(L)-1 or j == len(L[i])-1):
                L[i][j] *= multiplier
    L[1] = [2, 3]


li = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

print(li)
multiply_perimeter(li, 2)
print(li)


def max_diagonal_streak(L):
    max_value = 0
    for i in range(len(L)):
        counter = 1
        while ((i+counter) < len(L) and L[i][i] == L[i+counter][i+counter]):
            counter += 1
        if (counter > max_value):
            max_value = counter
    if (max_value == 1):
        return 0
    return max_value


li2 = [[8, 5, 3, 5, 3], [4, -8, 2, 54, 3],
       [-6, 4, 8, 75, 4], [5, 8, 5, 8, -4], [6, 4, 7, 4, 8]]


def max_diagonal_streak_two(L):
    max_value = 1
    for i in range(len(L)):
        counter = 1
        while ((counter+i) < len(L) and L[i][i] == L[i+counter][i+counter]):
            counter += 1
        if counter > max_value:
            max_value = counter
    if max_value == 1:
        return 0
    return max_value


# print(max_diagonal_streak_two(li2))
