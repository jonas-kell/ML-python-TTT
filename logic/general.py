import numpy as np

rows = 3

# assignmeint of variables:
# matrix is a rows x rows numpy array

# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transform to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transform to this state accordingly)


# returns 0 if undecided game
# returns 1 if 1s won game
# returns 2 if 2s won game
# returns 3 if draw
# hardcoded diagonals for 3x3 //TODO fix
def check_game_state(matrix):
    # test matrix shape
    if matrix.shape != (rows, rows):
        exit()

    # check rows
    for row in range(0, rows):
        if matrix[row, 0] != 0 and min(matrix[row, :]) == max(matrix[row, :]):
            return matrix[row, 0]

    # check columns
    for column in range(0, rows):
        if matrix[0, column] != 0 and min(matrix[:, column]) == max(matrix[:, column]):
            return matrix[0, column]

    # check diagonals
    if (
        matrix[0, 0] != 0
        and matrix[0, 0] == matrix[1, 1]
        and matrix[1, 1] == matrix[2, 2]
    ):
        return matrix[0, 0]
    if (
        matrix[0, 2] != 0
        and matrix[0, 2] == matrix[1, 1]
        and matrix[1, 1] == matrix[2, 0]
    ):
        return matrix[0, 2]

    # count 0s (open spots)
    for row in range(0, rows):
        for col in range(0, rows):
            if matrix[row][col] == 0:
                return 0
    return 3


# changes 1s and 2s in the matrix
def transpose_board(matrix):

    # test matrix shape
    if matrix.shape != (rows, rows):
        exit()

    # flip
    for row in range(0, rows):
        for column in range(0, rows):
            tmp = matrix[row][column]
            if tmp == 1:
                matrix[row][column] = 2
            elif tmp == 2:
                matrix[row][column] = 1

    return matrix