import game_logics as logic
import game_graphics as graphics
import game_ai as ai
import json
import pygame
import sys
import time

"""
This is the main module of the project Game-of-GO that connects the game logic and game graphics components with the user input
It contains methods that :
    -take the input from the user and decide what to do with it based on the environment
    -utilise the game_logics and game_graphics to modify the environment
    -map user input to logical input
    -define the main game loop
"""

# Variables that are used globally by this module
options = None  # contains the input dictionary of the game-options
first_player = None  # stores first player


def init_game():
    """
    Initialises the game options
    Orders the other modules to:
        Reads the game-options.json
        Initializes controller variables
        Initializes game logics
        Initializes graphical interface
        Commands Drawing of the Initial Board
        Commands Drawing of the Initial Scores
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
    player1_score, player2_score = logic.get_scores()
    graphics.draw_scores(player1_score,
                         player2_score)
    first_player = logic.get_turn()


def mouse_board_hover():
    """
    Gets mouse location from user
    Checks: if the mouse is located on the board
    Checks: if is on a valid position for the game and current player
    It commands the drawing of a hover image of the current player checker
    It also commands the deletion of the old hover image of the checker
    :return: None
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if graphics.mouse_on_board(mouse_x, mouse_y):
        board_x, board_y = graphics.get_board_pos_from_pixel_pos(mouse_x,
                                                                 mouse_y)
        if logic.is_legal_move(board_x, board_y):
            graphics.draw_mouse_hover(logic.get_turn(),
                                      board_x,
                                      board_y)
        else:
            graphics.delete_last_hover()
    else:
        graphics.delete_last_hover()


def update_board(board_removals, ko_add, ko_remove):
    """
    Orders the game_graphics to update the GUI board by
    deleting stones no longer existing and adding/removing KO checkers
    :param board_removals: may contain the positions on the board that no longer contain checkers
    :param ko_add: may contain the position in which a KO checker must be drawn
    :param ko_remove: may contain the old position of a KO checker
    :return: None
    """
    for change in board_removals:
        graphics.delete_stone(change[0],
                              change[1])
    if ko_add:
        graphics.draw_ko_block(logic.get_other_turn(),
                               ko_add[0],
                               ko_add[1])
    if ko_remove:
        graphics.delete_stone(ko_remove[0],
                              ko_remove[1])


def score_update():
    """
    Commands the update of the GUI score and GUI message withing game_graphics
    with the current score from the game_logic and the last player who completed their turn
    :return: None
    """
    player1_score, player2_score = logic.get_scores()
    graphics.draw_scores(player1_score,
                         player2_score)
    if logic.get_turn() == logic.get_player_checker(1):
        graphics.draw_message("Player1 moved",
                              error=False)
    else:
        graphics.draw_message("Player2 moved",
                              error=True)


def make_move(board_x, board_y):
    """
    Makes the move on the board on the position provided
    Commands game_logic to change and calculate the effects of the new move
    Commands game_graphics to adapt the GUI to the effects the move has generated
    :param board_x: x coordinate of the move on the board
    :param board_y: y coordinate of the move on the board
    :return: None
    """
    board_changes, ko_add, ko_remove = logic.move(board_x,
                                                  board_y)
    update_board(board_changes,
                 ko_add,
                 ko_remove)
    graphics.delete_last_hover()
    graphics.draw_stone(logic.get_turn(),
                        board_x,
                        board_y)
    score_update()
    logic.change_turn()


def human_make_move():
    """
    Takes input through mouse from human
    Using the game_graphics it maps the pixel input to board input
    Using game_logics it checks if it is a legal move for the current game
    Proceeds to committing the player move to the game
    :return: None
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if graphics.mouse_on_board(mouse_x, mouse_y):
        board_x, board_y = graphics.get_board_pos_from_pixel_pos(mouse_x,
                                                                 mouse_y)
        if logic.is_legal_move(board_x, board_y):
            make_move(board_x, board_y)


def winning():
    """
    Gets the scores and commands displaying a message on the GUI
    correspondent with the way the game has ended
    It allows the player/players to look at the final board
    and also allows them to quit the game the usual way
    :return: None
    """
    player1_score, player2_score = logic.get_scores()
    if player1_score > player2_score:
        message = "Player1 won!"
    elif player2_score > player1_score:
        message = "Player2 won!"
    else:
        message = "It's a tie!"
    graphics.draw_message(message)
    quited = False
    while not quited:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quited = True


def passing():
    """
    Commands displaying on the GUI the message correspondent to the player passing
    Commands the game_logic to pass the turn for the player
    Commands the Update of the GUI corresponding to effects
    :return:
    """
    if logic.get_turn() == logic.get_player_checker(1):
        graphics.draw_message("Player1 passed")
    else:
        graphics.draw_message("Player2 passed")
    logic.player_pass()
    graphics.delete_last_hover()


def start_game(opponent):
    """
    Contains the Initial Game loop with its events
    This is the method that interacts directly with the user input
    Depending on the action of the user, the controller chooses the way it
    orders the other modules to change the environment
    """
    clock = pygame.time.Clock()
    gaming = True
    while gaming:
        # Checks if the game is finished
        if logic.game_is_finished():
            winning()
            break
        # Game running on 60 fps
        clock.tick(60)
        # Drawing Mouse Board Hover
        mouse_board_hover()
        # User input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                human_make_move()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    passing()
        # If the user opted to play against computer
        if opponent == "computer" and logic.get_player_checker(1) != logic.get_turn():
            # Checks if the game is finished
            if logic.game_is_finished():
                winning()
                break
            # Gets the move from the AI and commits it
            move = ai.play_turn()
            make_move(move[0],
                      move[1])
    pygame.quit()


if __name__ == '__main__':
    init_game()
    # starts game vs human/computer
    start_game(sys.argv[1])
