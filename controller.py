import game_logics as logic
import game_graphics as graphics
import game_ai as AI
import json
import pygame
import sys

options = None
first_player = None


def init_game():
    """
    Initialises the game options
    Orders the other modules to:
        Initializes game logics
        Initializes graphical interface
        Draws Initial Board
        Draws Initial Scores
    """
    global options
    global first_player
    with open("game-options.json") as input:
        options = json.load(input)
    logic.initialise_game(options)
    pygame.init()
    pygame.display.set_caption(options["name"])
    graphics.initialise_game(options)
    graphics.draw_initial_board()
    scores = logic.get_scores()
    graphics.draw_scores(scores[0], scores[1])
    first_player = logic.get_turn()


def mouse_board_hover():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if graphics.mouse_on_board(mouse_x, mouse_y):
        board_x, board_y = graphics.get_board_position(mouse_x, mouse_y)
        if logic.is_legal_move(board_x, board_y):
            graphics.draw_mouse_hover(logic.get_turn(), board_x, board_y)
        else:
            graphics.delete_last_hover()
    else:
        graphics.delete_last_hover()


def make_move():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    graphics.delete_last_hover()
    if graphics.mouse_on_board(mouse_x, mouse_y):
        board_x, board_y = graphics.get_board_position(mouse_x, mouse_y)
        if logic.is_legal_move(board_x, board_y):
            logic.move(board_x,board_y)
            graphics.draw_stone(logic.get_turn(),board_x,board_y)
            logic.change_turn()
            if logic.get_turn() == 1:
                graphics.draw_message("Player2 moved",error=True)
            else:
                graphics.draw_message("Player1 moved", error=False)


def start_game(opponent):
    """
    Game loop and events
    This is the game loop in which the controller takes action input from the user
    Depending on the action of the user, the controller orders the other modules to change the environment
    """
    clock = pygame.time.Clock()
    gaming = True
    while gaming:
        clock.tick(60)
        mouse_board_hover()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                make_move()
        if opponent == "computer" and first_player != logic.get_turn():
            print("computer move")
            logic.change_turn()
    pygame.quit()


if __name__ == '__main__':
    init_game()
    start_game(sys.argv[1])
