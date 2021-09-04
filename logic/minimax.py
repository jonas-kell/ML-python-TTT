import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import check_game_state

rows = 3
# assignmeint of variables:
# matrix is a rows x rows numpy array

# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
# assumes there is space. may run into trouble if not the case
def get_next_move(matrix):
    # test matrix shape
    if matrix.shape != (rows, rows):
        raise ValueError("Wrong shapes")

    # AI to make its turn
    bestScore = -999999
    move = (-1, -1)

    for i in range(0, 3):
        for j in range(0, 3):
            # is avaliable?
            if matrix[i][j] == 0:
                matrix[i][j] = 1
                score = minimax(matrix, 0, False)
                matrix[i][j] = 0
                if score > bestScore:
                    bestScore = score
                    move = (i, j)

    # select best possibility
    matrix[move[0]][move[1]] = 1
    return matrix


# minimax implementation
def minimax(matrix, depth, isMaximizing):
    # grade outcome
    result = check_game_state(matrix)
    if result != 0:
        if result == 1:
            return +10
        elif result == 2:
            return -10
        else:
            return 0

    # recursive solver
    if isMaximizing:
        bestScore = -999999
        for i in range(0, 3):
            for j in range(0, 3):
                # is avaliable?
                if matrix[i][j] == 0:
                    matrix[i][j] = 1
                    score = minimax(matrix, depth + 1, False)
                    matrix[i][j] = 0
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = 999999
        for i in range(0, 3):
            for j in range(0, 3):
                # is avaliable?
                if matrix[i][j] == 0:
                    matrix[i][j] = 2
                    score = minimax(matrix, depth + 1, True)
                    matrix[i][j] = 0
                    bestScore = min(score, bestScore)
        return bestScore