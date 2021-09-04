import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import random_board
from logic.general import load_matrix_from_file
from logic.minimax_c import get_next_move as minimax_next_move
import logic.perceptron as perceptron

dim = 3

# cache function for many-times-execution
stored_weights1 = None
stored_weights2 = None

# assignmeint of variables:
# matrix is a 3 x 3 numpy array
# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
# assumes there is space. may run into trouble if not the case
def get_next_move(matrix):
    filename = "tic-tac-toe"

    # test matrix shape
    if matrix.shape != (dim, dim):
        raise ValueError("Wrong shapes")

    # cache control
    global stored_weights1
    global stored_weights2
    if stored_weights1 is None or stored_weights2 is None:
        stored_weights1 = load_matrix_from_file(filename + "1")
        stored_weights2 = load_matrix_from_file(filename + "2")

    # get propabilities
    results = ask_perceptron_and_format_solution(matrix)

    # find best move, that is allowed and on an empty position (== 0)
    best = (-1, -1)
    best_prob = -1
    for i in range(0, dim):
        for j in range(0, dim):
            if matrix[i, j] == 0:
                if results[i, j] > best_prob:
                    best_prob = results[i, j]
                    best = (i, j)

    matrix[best[0], best[1]] = 1
    return matrix


# expects stored weights to be set
def ask_perceptron_and_format_solution(matrix):
    global stored_weights1
    global stored_weights2

    # clone matrix, because it randomly gets modified otherwise
    use_matrix = np.copy(matrix)

    _, results = perceptron.get_output(
        use_matrix.reshape((dim * dim, 1)),
        stored_weights1,
        stored_weights2,
    )
    results = results.reshape((dim, dim))

    return results


# find the correct output-vector to a board in ml-1-(-1)-encoding
def get_minimax_expected_result(input):
    if input.shape != (9, 1):
        raise ValueError("Wrong shapes")

    # clone input, because it randomly gets modified otherwise
    use_input = np.copy(input)

    # get non-ml version of board
    state_before = use_input.reshape(3, 3)

    # get correct solution with minimax
    minimax_solution = np.copy(state_before)
    minimax_next_move(minimax_solution)

    # minimax will set one more 1 somewhere. Therefore the difference indicates the correct placement of the next digit
    expected = (minimax_solution - state_before).reshape((9, 1))

    return expected


# generate a random board state in ml-1-(-1)-encoding and the correct output-vector
def input_output_pair():
    # get random inputs in ml-format
    random_state = random_board(player1=1, player2=2)
    input = random_state.reshape((9, 1))

    # compute expected result
    expected_output = get_minimax_expected_result(input)

    return (input, expected_output)


if __name__ == "__main__":
    pass
    print(input_output_pair())
