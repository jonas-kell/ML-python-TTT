import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import check_game_state

# control the properties of the neural net
inputs = 9
outputs = 9
hidden = 5


# assignmeint of variables:
# matrix is a rows x rows numpy array

# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
# assumes there is space. may run into trouble if not the case
def get_next_move(matrix):
    pass


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


def get_output(input):

    weights1 = load_matrix_from_file("weights1")
    weights2 = load_matrix_from_file("weights2")

    if (
        input.shape != (inputs, 1)
        or weights1.shape != (hidden, inputs)
        or weights2.shape != (outputs, hidden)
    ):
        exit()

    return np.matmul(weights2, np.matmul(weights1, input))


store_matrix_to_file(np.ones((hidden, inputs)), "weights1")
store_matrix_to_file(np.ones((outputs, hidden)), "weights2")

print(get_output(np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9]])))