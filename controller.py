import game_logics as logic
import game_graphics as graphics
import game_ai as AI
import json
import pygame

options = None


def init_game():
    """
    Initialises the game options
    Orders the other modules to:
        Initializes game logics
        Initializes graphical interface
        Draws Initial Board
        Draws Initial Scores
    """
    with open("game-options.json") as input:
        options = json.load(input)
    logic.initialise_game(options)
    pygame.init()
    pygame.display.set_caption(options["name"])
    graphics.initialise_game(options)
    graphics.draw_initial_board()
    scores = logic.get_scores()
    graphics.draw_scores(scores[0], scores[1])


def start_game():
    """
    Game loop and events
    This is the game loop in which the controller takes action input from the user
    Depending on the action of the user, the controller orders the other modules to change the environment
    """
    gaming = True
    while gaming:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
    pygame.quit()


if __name__ == '__main__':
    init_game()
    start_game()
