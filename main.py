import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graphics.display_game import main as start_game
from logic.random_strat import get_next_move as random_next_move
from logic.minimax import get_next_move as minimax_next_move

start_game(minimax_next_move)