import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import check_game_state
from logic.general import random_board
from logic.general import flip_board
from logic.general import store_matrix_to_file
from logic.general import load_matrix_from_file
from logic.minimax_c import get_next_move as minimax_next_move

# control the properties of the neural net
dim = 3

inputs = dim * dim
outputs = dim * dim
hidden = 5
learn_rate = 0.005


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
    filename = "test"

    # test matrix shape
    if matrix.shape != (dim, dim):
        exit()

    # cache control
    global stored_weights1
    global stored_weights2
    if stored_weights1 is None or stored_weights2 is None:
        stored_weights1 = load_matrix_from_file(filename + "1")
        stored_weights2 = load_matrix_from_file(filename + "2")

    # get output works with the machine-learning coding, get_next_move doesn't
    flip_board(matrix, swap1=2, swap2=-1)
    _, results = get_output(
        matrix.reshape((dim * dim, 1)),
        stored_weights1,
        stored_weights2,
    )
    results = results.reshape((dim, dim))
    flip_board(matrix, swap1=2, swap2=-1)
    flip_board(results, swap1=2, swap2=-1)

    # find best move, that is allowed (empty position == 0)
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


def random_initial_matrices(filename):
    store_matrix_to_file(np.random.rand(hidden, inputs) * 2 - 1, filename + "1")
    store_matrix_to_file(np.random.rand(outputs, hidden) * 2 - 1, filename + "2")


def get_output(input, weights1, weights2):
    if (
        input.shape != (inputs, 1)
        or weights1.shape != (hidden, inputs)
        or weights2.shape != (outputs, hidden)
    ):
        exit()

    hidden_layer = tanh(np.matmul(weights1, input))
    result = sigmoid(np.matmul(weights2, hidden_layer))
    return (hidden_layer, result)


def update_weights_step(weights1, weights2):
    if weights1.shape != (hidden, inputs) or weights2.shape != (outputs, hidden):
        exit()

    # get random inputs in ml-format
    random_state = random_board(player1=1, player2=-1)
    input = random_state.reshape((inputs, 1))

    # compute best response
    (hidden_layer, result) = get_output(input, weights1, weights2)

    # compute expected result
    expected = get_minimax_expected_result(input)

    # compute deltas
    delta_end = expected - result
    delta_hidden_layer = (
        hidden_layer * (1 - hidden_layer) * np.matmul(weights2.T, delta_end)
    )  # sigmoid activated

    # update weights
    weights1 = weights1 + learn_rate * np.matmul(delta_hidden_layer, input.T)
    weights2 = weights2 + learn_rate * np.matmul(delta_end, hidden_layer.T)

    return (weights1, weights2)


def get_minimax_expected_result(input):
    if input.shape != (inputs, 1):
        exit()

    # get non-ml version of board
    state_before = flip_board(input.reshape(dim, dim), swap1=-1, swap2=2)

    minimax_solution = np.copy(state_before)
    minimax_next_move(minimax_solution)

    # minimax will set one more 1 somewhere. Therefore the difference indicates the correct placement of the next digit
    expected = (minimax_solution - state_before).reshape((inputs, 1))

    return expected


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


def train_perceptron(filename, iterations):
    # init the matrices
    # random_initial_matrices(filename)
    weights1 = load_matrix_from_file(filename + "1")
    weights2 = load_matrix_from_file(filename + "2")

    # perform leraning and update progress
    printed_percent = 0  # display only
    for i in range(0, iterations):
        # perform weight update for one step
        (weights1, weights2) = update_weights_step(weights1, weights2)

        percent = int(100.0 * i / iterations)
        if percent % 5 == 0 and percent != printed_percent:
            print("Training %d %% done" % percent)
            printed_percent = percent
            print(weights1[0, 0])

    # store the matrices for later use
    store_matrix_to_file(weights1, filename + "1")
    store_matrix_to_file(weights2, filename + "2")


if __name__ == "__main__":
    train_perceptron("test", 20000)
