import random
import numpy as np
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import store_as_json_to_file
from logic.general import load_as_json_from_file
from logic.general import number_to_board
from logic.general import board_to_number
from logic.general import check_game_state
from logic.minimax_c import get_next_move as minimax_next_move


# cache function for many-times-execution
cache = None

# assignmeint of variables:
# matrix is a 3 x 3 numpy array
# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
# assumes there is space. may run into trouble if not the case
def get_next_move(matrix):
    # test matrix shape
    if matrix.shape != (3, 3):
        raise ValueError("Wrong shapes")

    # cache control
    global cache
    if cache is None:
        cache = load_as_json_from_file("cache")

    # calc result where to move
    result = number_to_board(cache[str(board_to_number(matrix))]) - matrix
    for i in range(3):
        for j in range(3):
            if result[i][j] == 1:
                matrix[i][j] = 1
                break

    return matrix


# get a random board state and the correct output-vector from a precalculated lookup table
def random_precalculated_input_output_pair():
    # cache control
    global cache
    if cache is None:
        cache = load_as_json_from_file("cache")

    # get random inputs
    input_index = random.choice(list(cache.keys()))
    input = number_to_board(int(input_index))

    # compute expected result
    expected_output = number_to_board(int(cache[input_index]))

    return (input, expected_output)


# generate all possible boards and store their optimal solutions
def precalc_and_cache_input_output_pairs():
    calculated_cache = {}
    largest_board_number = 174762  # sum 2^(1+2n) from 0 to 8

    # perform cache and update progress
    printed_percent = 0  # display only
    for i in range(0, largest_board_number + 1):

        # get board
        board = number_to_board(i)

        # calc numbers in board
        unique, counts = np.unique(board, return_counts=True)
        occ = dict(zip(unique, counts))
        if 1 in occ.keys():
            ones = occ[1]
        else:
            ones = 0
        if 2 in occ.keys():
            twos = occ[2]
        else:
            twos = 0
        # check if valid board state
        if ones != twos and ones + 1 != twos:
            continue
        state = check_game_state(board)
        if state != 0:
            continue

        # board state is valid and usable for us
        calculated_cache[i] = board_to_number(minimax_next_move(board))

        # status update
        percent = int(100.0 * i / largest_board_number)
        if percent % 5 == 0 and percent != printed_percent:
            print("Caching %d %% done" % percent)
            printed_percent = percent

    store_as_json_to_file(calculated_cache, "cache")


if __name__ == "__main__":
    pass
    # precalc_and_cache_input_output_pairs()
