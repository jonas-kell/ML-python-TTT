import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import check_game_state
from logic.general import random_board
from logic.minimax_c import get_next_move as minimax_next_move

# control the properties of the neural net
inputs = 9
outputs = 9
hidden = 5

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
    dim = 3
    filename = "test"

    # test matrix shape
    if matrix.shape != (dim, dim):
        exit()

    global stored_weights1
    global stored_weights2

    if stored_weights1 is None or stored_weights2 is None:
        stored_weights1 = load_matrix_from_file(filename + "1")
        stored_weights2 = load_matrix_from_file(filename + "2")

    results = get_output(
        matrix.reshape((dim * dim, 1)), stored_weights1, stored_weights2
    ).reshape((dim, dim))

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

    return sigmoid(np.matmul(weights2, tanh(np.matmul(weights1, input))))


def update_weights_step(matrix, weights1, weights2):
    input = matrix.reshape((9, 1))
    if (
        input.shape != (inputs, 1)
        or weights1.shape != (hidden, inputs)
        or weights2.shape != (outputs, hidden)
    ):
        exit()

    # compute best response
    hidden_layer = tanh(np.matmul(weights1, input))
    result = sigmoid(np.matmul(weights2, hidden_layer))

    # compute expected result
    matrix_changed_minimax = np.copy(matrix)
    minimax_next_move(matrix_changed_minimax)
    # minimax will set one more 1 somewhere. Therefore the difference indicates the correct placement of the next digit
    expected = (matrix_changed_minimax - matrix).reshape((9, 1))

    # compute deltas
    delta_end = expected - result
    delta_hidden_layer = (
        hidden_layer * (1 - hidden_layer) * np.matmul(weights2.T, delta_end)
    )  # sigmoid activated

    # update weights
    learn_rate = 0.005
    weights1 = weights1 + learn_rate * np.matmul(delta_hidden_layer, input.T)
    weights2 = weights2 + learn_rate * np.matmul(delta_end, hidden_layer.T)

    return (weights1, weights2)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


def train_perceptron(filename, iterations):
    random_initial_matrices(filename)
    weights1 = load_matrix_from_file(filename + "1")
    weights2 = load_matrix_from_file(filename + "2")

    printed_percent = 0
    for i in range(0, iterations):
        # get setup
        matrix = random_board()
        # perform weight update for one step
        (weights1, weights2) = update_weights_step(matrix, weights1, weights2)

        percent = int(100.0 * i / iterations)
        if percent % 5 == 0 and percent != printed_percent:
            print("Training %d %% done" % percent)
            printed_percent = percent
            print(weights1[0, 0])

    store_matrix_to_file(weights1, filename + "1")
    store_matrix_to_file(weights2, filename + "2")


if __name__ == "__main__":
    train_perceptron("test", 25000)
