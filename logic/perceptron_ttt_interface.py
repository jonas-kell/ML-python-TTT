import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import random_board
from logic.general import load_matrix_from_file
from logic.minimax_c import get_next_move as minimax_next_move
from logic.cache_minimax import random_precalculated_input_output_pair
import logic.perceptron as perceptron

dim = 3

# assignmeint of variables:
# matrix is a 3 x 3 numpy array
# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
# assumes there is space. may run into trouble if not the case
def get_next_move(matrix):
    # test matrix shape
    if matrix.shape != (dim, dim):
        raise ValueError("Wrong shapes")

    # get propabilities
    # clone matrix, because it randomly gets modified otherwise
    copied_matrix = np.copy(matrix)

    results = perceptron.get_output_simple(copied_matrix.reshape((dim * dim, 1)))
    results = results.reshape((dim, dim))

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


# generate a random board state and the correct output-vector
def random_input_output_pair():
    input_square, out_square = random_precalculated_input_output_pair()

    return (
        input_square.reshape(dim * dim, 1),
        (out_square - input_square).reshape(dim * dim, 1),
    )
