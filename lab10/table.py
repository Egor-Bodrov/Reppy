def row_sums(matrix):
    return [sum(row) for row in matrix]


def column_sums(matrix):
    if not matrix:
        return []
    columns = len(matrix[0])
    return [sum(row[column] for row in matrix) for column in range(columns)]