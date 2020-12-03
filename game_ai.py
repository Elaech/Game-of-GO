import random
import game_logics as logic
import time

"""
This is the module that handles the AI that plays go against humans
It contains methods that help the AI decide on a move to make considering the current situation
"""


def get_available_moves():
    """
    Searches the space of moves on the table
    and returns a list of the legal moves for the AI on the board
    :return: list of all available positions at which the AI can make a move
    """
    output = []
    for index_x in range(logic.get_board_size()):
        for index_y in range(logic.get_board_size()):
            if logic.is_legal_move(index_x, index_y):
                output.append([index_x, index_y])
    return output


def play_turn():
    """
    Chooses randomly a position from the available position for the AI
    :return: chosen position to play at
    """
    available_moves = get_available_moves()
    # Gives a little time between moves to improve player experience
    time.sleep(0.5)
    return random.choice(available_moves)
