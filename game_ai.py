"""

"""

import random
import game_logics as logic
import time

def get_available_moves():
    output = []
    for index_x in range(logic.get_board_size()):
        for index_y in range(logic.get_board_size()):
            if logic.is_legal_move(index_x, index_y):
                output.append([index_x, index_y])
    return output


def play_turn():
    available_moves = get_available_moves()
    time.sleep(0.5)
    return random.choice(available_moves)
