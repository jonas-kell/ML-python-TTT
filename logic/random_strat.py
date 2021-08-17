import numpy as np
import random

rows = 3
random.seed(200)

# assignmeint of variables:
# matrix is a rows x rows numpy array

# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
# assumes there is space. may run into trouble if not the case
def get_next_move(matrix):
    # test matrix shape
    if matrix.shape != (rows, rows):
        exit()

    while True:
        row = random.randrange(rows)
        column = random.randrange(rows)

        if matrix[row][column] == 0:
            matrix[row][column] = 1
            break

    return matrix