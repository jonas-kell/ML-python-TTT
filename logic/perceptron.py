import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import check_game_state
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

    if stored_weights1 == None or stored_weights2 == None:
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

    matrix[i, j] = 1


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


def get_output(input, weights1, weights2):
    if (
        input.shape != (inputs, 1)
        or weights1.shape != (hidden, inputs)
        or weights2.shape != (outputs, hidden)
    ):
        exit()

    return sigmoid(np.matmul(weights2, tanh(np.matmul(weights1, input))))


def random_initial_matrices(filename):
    store_matrix_to_file(np.random.rand(hidden, inputs) * 2 - 1, filename + "1")
    store_matrix_to_file(np.random.rand(outputs, hidden) * 2 - 1, filename + "2")


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


# random_initial_matrices("test")

# get_next_move(np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]]))
