import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import store_matrix_to_file
from logic.general import load_matrix_from_file
import logic.perceptron_ttt_interface as interface

# control the properties of the neural net
inputs = 2
outputs = 1
hidden = 3
learn_rate = 0.01


def random_initial_matrices(filename):
    store_matrix_to_file(np.random.rand(hidden, inputs) * 2 - 1, filename + "1")
    store_matrix_to_file(np.random.rand(outputs, hidden) * 2 - 1, filename + "2")


def get_output(input, weights1, weights2):
    if (
        input.shape != (inputs, 1)
        or weights1.shape != (hidden, inputs)
        or weights2.shape != (outputs, hidden)
    ):
        raise ValueError("wrong shapes")

    hidden_layer = tanh(np.matmul(weights1, input))
    result = sigmoid(np.matmul(weights2, hidden_layer))
    return (hidden_layer, result)


def update_weights_step(weights1, weights2, input, expected_output):
    if (
        input.shape != (inputs, 1)
        or expected_output.shape != (outputs, 1)
        or weights1.shape != (hidden, inputs)
        or weights2.shape != (outputs, hidden)
    ):
        raise ValueError("wrong shapes")

    # compute perceptron response
    (hidden_layer, result) = get_output(input, weights1, weights2)

    # compute deltas
    delta_end = result * (1 - result) * (expected_output - result)  # sigmoid activated
    delta_hidden_layer = (
        (1 + hidden_layer) * (1 - hidden_layer) * np.matmul(weights2.T, delta_end)
    )  # tanh activated

    # update weights
    weights1 = weights1 + learn_rate * np.matmul(delta_hidden_layer, input.T)
    weights2 = weights2 + learn_rate * np.matmul(delta_end, hidden_layer.T)

    return (weights1, weights2)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


def train_perceptron(filename, iterations, input_output_pair):
    # init the matrices
    # random_initial_matrices(filename)
    weights1 = load_matrix_from_file(filename + "1")
    weights2 = load_matrix_from_file(filename + "2")

    # perform leraning and update progress
    printed_percent = 0  # display only
    for i in range(0, iterations):
        # input and corresponding solution
        input, expected_output = input_output_pair()

        # perform weight update for one step
        (weights1, weights2) = update_weights_step(
            weights1, weights2, input, expected_output
        )

        percent = int(100.0 * i / iterations)
        if percent % 5 == 0 and percent != printed_percent:
            print("Training %d %% done" % percent)
            printed_percent = percent
            print(weights1[0, 0])

    # store the matrices for later use
    store_matrix_to_file(weights1, filename + "1")
    store_matrix_to_file(weights2, filename + "2")


def learn_and():
    import random

    res = [
        (np.array([[0], [0]]), np.array([[1]])),
        (np.array([[1], [0]]), np.array([[1]])),
        (np.array([[0], [1]]), np.array([[1]])),
        (np.array([[1], [1]]), np.array([[0]])),
    ]
    return res[random.randint(0, 3)]


if __name__ == "__main__":
    # train_perceptron("test", 100000, interface.input_output_pair)

    train_perceptron("test", 100000, learn_and)

    print(
        get_output(
            np.array([[0], [0]]),
            load_matrix_from_file("test1"),
            load_matrix_from_file("test2"),
        )[1]
    )
    print(
        get_output(
            np.array([[1], [0]]),
            load_matrix_from_file("test1"),
            load_matrix_from_file("test2"),
        )[1]
    )
    print(
        get_output(
            np.array([[0], [1]]),
            load_matrix_from_file("test1"),
            load_matrix_from_file("test2"),
        )[1]
    )
    print(
        get_output(
            np.array([[1], [1]]),
            load_matrix_from_file("test1"),
            load_matrix_from_file("test2"),
        )[1]
    )
