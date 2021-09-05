import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.random_strat import get_next_move as random_next_move
from logic.minimax_c import get_next_move as minimax_next_move
from logic.perceptron_ttt_interface import get_next_move as perceptron_next_move
from logic.cache_minimax import get_next_move as minimax_cached_next_move

from logic.general import check_game_state
from logic.general import flip_board

print("Compare Algorithms:")

algorithm1 = perceptron_next_move
algorithm2 = random_next_move

algorithm1wins = 0
algorithm2wins = 0
draws = 0

games = 5000

for i in range(games):
    matrix = np.zeros((3, 3), dtype=np.int8)
    result = 0
    index = 0
    if i % 2 == 0:
        index = 1
    while result == 0:
        # make a move
        if index % 2 == 0:
            algorithm1(matrix)
        else:
            flip_board(matrix)
            algorithm2(matrix)
            flip_board(matrix)

        # check results
        result = check_game_state(matrix)
        if result == 1:
            algorithm1wins += 1
        if result == 2:
            algorithm2wins += 1
        if result == 3:
            draws += 1
        index += 1

print("algorithm 1 won: %d %%" % int(100.0 * algorithm1wins / games))
print("algorithm 2 won: %d %%" % int(100.0 * algorithm2wins / games))
print("Draws: %d %%" % int(100.0 * draws / games))
