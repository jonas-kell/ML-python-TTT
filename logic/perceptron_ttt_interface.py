import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import random_board
from logic.general import load_matrix_from_file
from logic.minimax_c import get_next_move as minimax_next_move
from logic.cache_minimax import random_precalculated_input_output_pair
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


# generate a random board state and the correct output-vector
def random_input_output_pair():
    input_square, out_square = random_precalculated_input_output_pair()

    return (
        input_square.reshape(dim * dim, 1),
        (out_square - input_square).reshape(dim * dim, 1),
    )
