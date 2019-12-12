def negate(matrix):
    return_matrix = matrix[:]
    for i in range(len(return_matrix)):
        for j in range(len(return_matrix[i])):
            if i > j:
                return_matrix[i][j] *= -1
    return return_matrix


print(negate([[1, 2, 3], [4, 6, 7], [8, 4, 3]]))
