import numpy as np
import random

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
# hardcoded diagonals for 3x3 //TODO fix (becomes very slow because of pathetic python for loops...)
def check_game_state(matrix):
    # test matrix shape
    if matrix.shape != (rows, rows):
        exit()

    # check rows
    for row in range(0, rows):
        if (
            matrix[row, 0] != 0
            and matrix[row, 0] == matrix[row, 1]
            and matrix[row, 1] == matrix[row, 2]
        ):
            return matrix[row, 0]

    # check columns
    for column in range(0, rows):
        if (
            matrix[0, column] != 0
            and matrix[0, column] == matrix[1, column]
            and matrix[1, column] == matrix[2, column]
        ):
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
def flip_board(matrix):

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


# changes -1s and 1s in the matrix
def flip_ml_board(matrix):

    # test matrix shape
    if matrix.shape != (rows, rows):
        exit()

    # flip
    for row in range(0, rows):
        for column in range(0, rows):
            tmp = matrix[row][column]
            if tmp == -1:
                matrix[row][column] = 1
            elif tmp == 1:
                matrix[row][column] = -1

    return matrix


# changes -1s and 2s in the matrix
def transform_to_from_ml(matrix):

    # test matrix shape
    if matrix.shape != (rows, rows):
        exit()

    # flip
    for row in range(0, rows):
        for column in range(0, rows):
            tmp = matrix[row][column]
            if tmp == -1:
                matrix[row][column] = 2
            elif tmp == 2:
                matrix[row][column] = -1

    return matrix


# generates a random board state from the point of the 1s perspective
# (next turn always belongs to 1)
def random_board():
    # who starts?
    turn = random.randint(1, 2)

    # number of turns (0 to 8) if 1 (you) started and (1 to 7) if 2 (oppponent) started
    turns = 0
    if turn == 1:
        turns = random.randint(0, 8)
    else:
        turns = random.randint(1, 7)

    # try boards and find one without winner and random specs
    state = -1
    while state != 0:
        matrix = np.zeros((rows, rows), dtype=np.int8)

        for i in range(0, turns):
            # set randomly (not efficient)
            while True:
                row = random.randrange(rows)
                column = random.randrange(rows)
                if matrix[row][column] == 0:
                    matrix[row][column] = turn
                    break
            if turn == 1:
                turn = 2
            else:
                turn = 1

        state = check_game_state(matrix)

    return matrix