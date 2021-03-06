import os, sys
import random
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import store_matrix_to_file
from logic.general import load_matrix_from_file
import logic.perceptron_ttt_interface as interface

# cache function for many-times-execution
stored_weights1 = None
stored_bias_1 = None
stored_weights2 = None

# control the properties of the neural net
inputs = 9
outputs = 9
hidden = 30
learn_rate = 0.0001


def random_initial_matrices(filename):
    store_matrix_to_file(np.random.rand(hidden, inputs) * 2 - 1, filename + "1")
    store_matrix_to_file(np.random.rand(hidden, 1) * 2 - 1, filename + "1b")
    store_matrix_to_file(np.random.rand(outputs, hidden) * 2 - 1, filename + "2")


def get_output_simple(input, filename="tic-tac-toe"):
    # cache control
    global stored_weights1
    global stored_bias_1
    global stored_weights2
    if stored_weights1 is None or stored_bias_1 is None or stored_weights2 is None:
        stored_weights1 = load_matrix_from_file(filename + "1")
        stored_bias_1 = load_matrix_from_file(filename + "1b")
        stored_weights2 = load_matrix_from_file(filename + "2")

    _, results = get_output(input, stored_weights1, stored_bias_1, stored_weights2)

    return results


def get_output(input, weights1, bias1, weights2):
    if (
        input.shape != (inputs, 1)
        or weights1.shape != (hidden, inputs)
        or bias1.shape != (hidden, 1)
        or weights2.shape != (outputs, hidden)
    ):
        raise ValueError("Wrong shapes")

    hidden_layer = sigmoid(np.matmul(weights1, input) + bias1)
    result = sigmoid(np.matmul(weights2, hidden_layer))
    return (hidden_layer, result)


def update_weights_step(weights1, bias1, weights2, input, expected_output):
    if (
        input.shape != (inputs, 1)
        or expected_output.shape != (outputs, 1)
        or weights1.shape != (hidden, inputs)
        or bias1.shape != (hidden, 1)
        or weights2.shape != (outputs, hidden)
    ):
        raise ValueError("Wrong shapes")

    # compute perceptron response
    (hidden_layer, result) = get_output(input, weights1, bias1, weights2)

    # compute deltas
    delta_end = result * (1 - result) * (expected_output - result)  # sigmoid activated

    delta_hidden_layer = (
        hidden_layer * (1 - hidden_layer) * np.matmul(weights2.T, delta_end)
    )  # sigmoid activated

    # update weights
    weights1 = weights1 + learn_rate * np.matmul(delta_hidden_layer, input.T)
    bias1 = bias1 + learn_rate * delta_hidden_layer
    weights2 = weights2 + learn_rate * np.matmul(delta_end, hidden_layer.T)

    return (weights1, bias1, weights2)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def train_perceptron(filename, iterations, input_output_pair, init_random=True):
    # init the matrices
    if init_random:
        random_initial_matrices(filename)

    weights1 = load_matrix_from_file(filename + "1")
    bias1 = load_matrix_from_file(filename + "1b")
    weights2 = load_matrix_from_file(filename + "2")

    # test shapes
    if (
        input_output_pair()[0].shape != (inputs, 1)
        or input_output_pair()[1].shape != (outputs, 1)
        or weights1.shape != (hidden, inputs)
        or bias1.shape != (hidden, 1)
        or weights2.shape != (outputs, hidden)
    ):
        raise ValueError("Wrong shapes")

    # perform leraning and update progress
    printed_percent = 0  # display only
    for i in range(0, iterations):
        # input and corresponding solution
        input, expected_output = input_output_pair()

        # perform weight update for one step
        (weights1, bias1, weights2) = update_weights_step(
            weights1, bias1, weights2, input, expected_output
        )

        percent = int(100.0 * i / iterations)
        if percent % 5 == 0 and percent != printed_percent:
            print("Training %d %% done" % percent)
            printed_percent = percent

    # store the matrices for later use
    store_matrix_to_file(weights1, filename + "1")
    store_matrix_to_file(bias1, filename + "1b")
    store_matrix_to_file(weights2, filename + "2")


def learn_logic():
    res = [
        (np.array([[0], [0], [0]]), np.array([[0]])),
        (np.array([[1], [0], [0]]), np.array([[1]])),
        (np.array([[0], [1], [0]]), np.array([[1]])),
        (np.array([[1], [1], [0]]), np.array([[0]])),
        (np.array([[0], [0], [1]]), np.array([[0]])),
        (np.array([[1], [0], [1]]), np.array([[1]])),
        (np.array([[0], [1], [1]]), np.array([[1]])),
        (np.array([[1], [1], [1]]), np.array([[0]])),
    ]
    return res[random.randint(0, 7)]


def learn_logic_test():
    global inputs
    global outputs
    global hidden
    global learn_rate

    inputs = 3
    outputs = 1
    hidden = 20
    learn_rate = 0.01

    train_perceptron("logic", 200000, learn_logic, init_random=True)

    for i in range(0, 8):
        print(
            get_output_simple(
                [
                    np.array([[0], [0], [0]]),
                    np.array([[1], [0], [0]]),
                    np.array([[0], [1], [0]]),
                    np.array([[1], [1], [0]]),
                    np.array([[0], [0], [1]]),
                    np.array([[1], [0], [1]]),
                    np.array([[0], [1], [1]]),
                    np.array([[1], [1], [1]]),
                ][i],
                "logic",
            )
        )


if __name__ == "__main__":
    # learn_logic_test()  # test the leraning process with a simple demo

    train_perceptron(
        "tic-tac-toe", 80000, interface.random_input_output_pair, init_random=False
    )