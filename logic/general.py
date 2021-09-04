import numpy as np
import random
import json

rows = 3

# assignmeint of variables:
# matrix is a rows x rows numpy array

# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transform to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transform to this state accordingly)


# returns 0 if undecided game
# returns 1 if player1 won game
# returns 2 if player2 won game
# returns 3 if draw
# hardcoded diagonals for 3x3 //TODO fix (becomes very slow because of pathetic python for loops...)
def check_game_state(matrix, player1=1, player2=2):
    # test matrix shape
    if matrix.shape != (rows, rows):
        raise ValueError("Wrong shapes")

    # check rows
    for row in range(0, rows):
        if matrix[row, 0] == matrix[row, 1] and matrix[row, 1] == matrix[row, 2]:
            if matrix[row, 0] == player1:
                return 1
            elif matrix[row, 0] == player2:
                return 2

    # check columns
    for column in range(0, rows):
        if (
            matrix[0, column] == matrix[1, column]
            and matrix[1, column] == matrix[2, column]
        ):
            if matrix[0, column] == player1:
                return 1
            elif matrix[0, column] == player2:
                return 2

    # check diagonals
    if (matrix[0, 0] == matrix[1, 1] and matrix[1, 1] == matrix[2, 2]) or (
        matrix[0, 2] == matrix[1, 1] and matrix[1, 1] == matrix[2, 0]
    ):
        if matrix[1, 1] == player1:
            return 1
        elif matrix[1, 1] == player2:
            return 2

    # count 0s (open spots)
    for row in range(0, rows):
        for col in range(0, rows):
            if matrix[row][col] == 0:
                return 0
    return 3


# changes 1s and 2s in the matrix
def flip_board(matrix, swap1=1, swap2=2):

    # test matrix shape
    if matrix.shape != (rows, rows):
        raise ValueError("Wrong shapes")

    # flip
    for row in range(0, rows):
        for column in range(0, rows):
            tmp = matrix[row][column]
            if tmp == swap1:
                matrix[row][column] = swap2
            elif tmp == swap2:
                matrix[row][column] = swap1

    return matrix


# generates a random board state from the point of the player1's perspective
# (next turn always belongs to player1)
def random_board(player1=1, player2=2):
    # who starts?
    turn = random.randint(1, 2)

    # number of turns (0 to 8) if 1 (you) started and (1 to 7) if 2 (oppponent) started
    turns = 0
    if turn == 1:
        turn = player1
        turns = random.randint(0, 8)
    else:
        turn = player2
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
            if turn == player1:
                turn = player2
            else:
                turn = player1

        state = check_game_state(matrix)

    return matrix


def store_matrix_to_file(matrix, filename):
    file = open("storage/" + filename + ".txt", "w")
    rows, columns = matrix.shape
    file.writelines(str(rows) + "\n")
    file.write(str(columns) + "\n")
    for number in matrix.flatten():
        file.write(str(number) + "\n")
    file.close()


def load_matrix_from_file(filename):
    file = open("storage/" + filename + ".txt", "r")
    lines = file.readlines()
    numbers = [None] * len(lines)
    for i, line in enumerate(lines):
        numbers[i] = float(line)
    result = np.reshape(numbers[2:], (int(numbers[0]), int(numbers[1])))
    file.close()
    return result


def store_as_json_to_file(obj, filename):
    file = open("storage/" + filename + ".json", "w")
    file.write(json.dumps(obj, separators=(",", ":")))
    file.close()


def load_as_json_from_file(filename):
    file = open("storage/" + filename + ".json", "r")
    line = file.readline()
    result = json.loads(line)

    file.close()
    return result


def board_to_number(matrix, player1=1, player2=2):
    # test matrix shape
    if matrix.shape != (rows, rows):
        raise ValueError("Wrong shapes")

    number = 0
    mask = 1
    for element in matrix.flatten():
        if element == player1:
            number = number | mask
        mask = mask << 1
        if element == player2:
            number = number | mask
        mask = mask << 1

    return number


def number_to_board(number, player1=1, player2=2):
    matrix = np.zeros((rows * rows), dtype=np.int8)

    mask = 1
    for i in range(rows * rows):
        if (number & mask) != 0:
            matrix[i] = player1
        mask = mask << 1
        if (number & mask) != 0:
            matrix[i] = player2
        mask = mask << 1

    return matrix.reshape((rows, rows))