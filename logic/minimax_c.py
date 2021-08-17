import os, sys
import numpy as np
import ctypes as ct

rows = 3

# assignmeint of variables:
# matrix is a rows x rows numpy array

# a 0 indicates no placed symbol
# a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
# a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
# assumes there is space. may run into trouble if not the case
def get_next_move(matrix):

    # re-generate the c file if you make changes:
    # gcc -fPIC -shared -o ./logic/minimax.dll ./logic/minimax.c

    # load c function into memory
    dll_file = (
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        + "\logic\minimax.dll"
    )
    lib = ct.CDLL(dll_file)

    # create c-int-array and put in values via spread operator
    IntArray9 = ct.c_int * 9  # define new type that is an array of 9 ints
    arr = IntArray9(*(matrix.flatten()))

    # call c-function
    lib.best_position(arr)

    # parse result from c-function
    for i in range(3):
        for j in range(3):
            matrix[i][j] = arr[3 * i + j]

    return matrix
