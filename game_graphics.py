import pygame
import pygame.freetype

"""
This is the graphical module for the project Game-Of-GO
It contains methods for initializing and drawing on the GUI
The GUI for the project consists of mainly 3 parts:
    The Board for the game
    The Scores of the players
    A place to display game messages/errors
"""

# Variables that are used globally by this module
board_size = None
board_pixel_size = None
line_color = None
font = None
score_pixel_size = None
game_screen = None
checker_pixel_size = None
background_color = None
player_colors = None
upper_board_margin = None
lower_board_margin = None
line_thickness = None
valid_color = None
invalid_color = None
last_hover = None
checker_hover_pixel_radius = None
checker_pixel_radius = None
ko_pixel_length = None
score_padding = None


def initialise_game(options):
    """
    Initialises all global variables that are needed for drawing anything on the user interface
    The values for initialisation are received from the controller
    It also creates the game screen on which all the elements are drawn
    :param options: information from the controller concerning pixels, sizes, fonts, colors given as a dictionary
    :return: None
    """
    global game_screen
    global board_size
    global checker_pixel_size
    global board_pixel_size
    global line_color
    global font
    global score_pixel_size
    global background_color
    global player_colors
    global upper_board_margin
    global lower_board_margin
    global score_padding
    global line_thickness
    global valid_color
    global invalid_color
    global checker_hover_pixel_radius
    global checker_pixel_radius
    global ko_pixel_length
    board_size = options["board-size"]
    checker_pixel_size = options["checker-pixel-size"]
    board_pixel_size = (board_size + 1) * checker_pixel_size
    line_color = options["line-color"]
    invalid_color = options["invalid-color"]
    valid_color = options["valid-color"]
    score_pixel_size = options["score-pixel-size"]
    font = pygame.freetype.SysFont("Arial",
                                   score_pixel_size / 2)  # Font will take only half of the vertical space of the score
    upper_board_margin = checker_pixel_size
    lower_board_margin = checker_pixel_size * board_size
    background_color = options["background-color"]
    player_colors = options["player-colors"]
    line_thickness = options["line-thickness"]
    score_padding = score_pixel_size / 8  # Padding used for distancing the score from other margins
    ko_pixel_length = checker_pixel_size / 3  # KO Checker length
    checker_hover_pixel_radius = checker_pixel_size / 3
    checker_pixel_radius = checker_pixel_size / 2 - 2  # Checker Radius
    game_screen = pygame.display.set_mode((board_pixel_size,
                                           board_pixel_size + score_pixel_size))  # Initialize screen


def draw_initial_board():
    """
    Draws the initial empty board according the already initialized piece/table/font colors and sizes
    :return: None
    """
    game_screen.fill(background_color)
    for position in range(board_size):
        varying_position = (1 + position) * checker_pixel_size
        pygame.draw.line(game_screen,
                         line_color,
                         (varying_position, upper_board_margin),
                         (varying_position, lower_board_margin),
                         line_thickness)

        pygame.draw.line(game_screen,
                         line_color,
                         (upper_board_margin, varying_position),
                         (lower_board_margin, varying_position),
                         line_thickness)
    pygame.display.update()


def draw_scores(player1_score, player2_score):
    """
    Draws the score part of the user interface given the two player scores
    This part is visibile under the board and it consists in 3 parts: player1score, player2score, and error_msg
    :param player1_score: player1 score
    :param player2_score: player2 score
    :return: None
    """
    # Deleting old scores
    pygame.draw.rect(game_screen,
                     background_color,
                     [0, board_pixel_size, board_pixel_size, board_pixel_size + score_pixel_size])
    # Drawing the outer frames
    pygame.draw.rect(game_screen,
                     player_colors[0],
                     [score_padding, board_pixel_size - score_padding, score_pixel_size * 2.5,
                      score_pixel_size - score_padding],
                     line_thickness)
    pygame.draw.rect(game_screen,
                     player_colors[1],
                     [score_pixel_size * 2.5 + score_padding * 2, board_pixel_size - score_padding,
                      score_pixel_size * 2.5,
                      score_pixel_size - score_padding],
                     line_thickness)
    # Drawing the text within the frames
    font.render_to(game_screen,
                   (score_padding * 2, board_pixel_size + score_padding),
                   "Player1: " + str(player1_score),
                   player_colors[0])
    font.render_to(game_screen,
                   (score_pixel_size * 2.5 + score_padding * 4, board_pixel_size + score_padding),
                   "Player2: " + str(player2_score),
                   player_colors[1])
    pygame.display.update()


def draw_message(message, error=False):
    """
    Draws message on the message part of the GUI with color depending of error parameter
    :param message: text to be drawn
    :param error: True - it is an error, False - it is not an error
    :return: None
    """
    pygame.draw.rect(game_screen,
                     background_color,
                     [score_pixel_size * 5 + score_padding * 4, board_pixel_size + score_padding, board_pixel_size,
                      board_pixel_size + score_pixel_size])
    # Adapting text color
    color = valid_color
    if error:
        color = invalid_color
    # Drawing the text in its respective area
    font.render_to(game_screen,
                   (score_pixel_size * 5 + score_padding * 4, board_pixel_size + score_padding),
                   message,
                   color)
    pygame.display.update()


def draw_stone(turn, board_x, board_y):
    """
    Given a player turn and a position on board it draws
    a player stone with corresponding color
    :param turn: current player turn
    :param board_x: x coordinate on board
    :param board_y: y coordinate on board
    :return: None
    """
    # Getting player color
    color = player_colors[turn]
    # Transforming board coordinates to pixel coordinates
    x_pixel, y_pixel = get_pixel_pos_from_board_pos(board_x,
                                                    board_y)
    # Drawing the stone
    pygame.draw.circle(game_screen,
                       color,
                       [x_pixel, y_pixel],
                       checker_pixel_radius)
    pygame.display.update()


def delete_stone(board_x, board_y):
    """
    Given a board position it empties it by drawing an empty space
    :param board_x: x cooordinate on board
    :param board_y: y coordinate on board
    :return: None
    """
    # Transforming coordinates to pixel coordinates
    pixel_x, pixel_y = get_pixel_pos_from_board_pos(board_x,
                                                    board_y)
    # Draws empty space
    draw_empty_pixel_pos(pixel_x,
                         pixel_y)


def draw_empty_pixel_pos(x_pixel, y_pixel):
    """
    Given a pair of pixel coordinates it draws an empty position corresponding to
    the Game-Of-GO:
    interior position: circle with background color with a cross formed with lines in its center
    exterior position: interior position but without one part of the cross
    :param x_pixel: x pixel coordinate
    :param y_pixel: y pixel coordinate
    :return: None
    """
    # Emptying Space
    pygame.draw.circle(game_screen,
                       background_color,
                       [x_pixel, y_pixel],
                       checker_pixel_radius)
    # Normalising the dimensions of the Cross based on pixel coordinates
    north = max(y_pixel - checker_pixel_radius,
                checker_pixel_size)
    south = min(y_pixel + checker_pixel_radius,
                board_pixel_size - checker_pixel_size)
    east = max(x_pixel - checker_pixel_radius,
               checker_pixel_size)
    west = min(x_pixel + checker_pixel_radius,
               board_pixel_size - checker_pixel_size)
    # Drawing the Cross
    pygame.draw.line(game_screen,
                     line_color,
                     [x_pixel, south],
                     [x_pixel, north],
                     line_thickness)
    pygame.draw.line(game_screen,
                     line_color,
                     [east, y_pixel],
                     [west, y_pixel],
                     line_thickness)
    pygame.display.update()


def draw_ko_block(turn, board_x, board_y):
    """
    Given a player turn for the color
    and a position on board it draw a KO block.
    A KO block represents a square centered on a position
    that has the color of the player that is being KO-ed
    :param turn: player turn
    :param board_x: x coordinate on board
    :param board_y: y coordinate on board
    :return: None
    """
    # Getting correspondent color
    color = player_colors[turn]
    # Transforming coordinates to pixel coordinates
    x_pixel, y_pixel = get_pixel_pos_from_board_pos(board_x,
                                                    board_y)
    # Drawing the KO Piece - Empty Centered Square
    pygame.draw.rect(game_screen,
                     color,
                     [x_pixel - ko_pixel_length,
                      y_pixel - ko_pixel_length,
                      2 * ko_pixel_length,
                      2 * ko_pixel_length],
                     line_thickness)
    pygame.display.update()


def get_board_pos_from_pixel_pos(mouse_x, mouse_y):
    """
    Given some pixel coordinates on the game board
    it returns the specific board coordinates
    :param mouse_x: x pixel coordinate
    :param mouse_y: y pixel coordinate
    :return: x board coordinate, y board coordinate
    """
    x_pos = int((mouse_x - checker_pixel_size / 2) / checker_pixel_size)
    y_pos = int((mouse_y - checker_pixel_size / 2) / checker_pixel_size)
    return x_pos, y_pos


def get_pixel_pos_from_board_pos(board_x, board_y):
    """
    Given some board coordinates from the game board
    it returns the specific pixel coordinates
    :param board_x: x coordinate of board
    :param board_y: y coordinate of board
    :return: x pixel coordinate, y pixel coordinate
    """
    x_pos = board_x * checker_pixel_size + checker_pixel_size
    y_pos = board_y * checker_pixel_size + checker_pixel_size
    return x_pos, y_pos


def mouse_on_board(mouse_x, mouse_y):
    """
    Given some pixel coordinates it returns whether the mouse is on the game board or not
    :param mouse_x:
    :param mouse_y:
    :return: True - mouse on board / False - mouse not on board
    """
    # Checking the mouse coordinates against boarder margins
    return (board_pixel_size - checker_pixel_size / 2) > mouse_y > (checker_pixel_size / 2) \
           and (checker_pixel_size / 2) < mouse_x < (board_pixel_size - checker_pixel_size / 2)


def delete_last_hover():
    """
    Deletes the last drawn hover from the game board if it exists
    :return: None
    """
    global last_hover
    if last_hover:
        draw_empty_pixel_pos(last_hover[0],
                             last_hover[1])
    last_hover = None


def draw_mouse_hover(turn, board_x, board_y):
    """
    Given a player turn and a position on the board
    it draws a smaller checker (hover checker)
    over the position the cursor is currently on
    :param turn: player turn
    :param board_x: x coordinate on board
    :param board_y: y coordinate on board
    :return: None
    """
    global last_hover
    # Getting player color
    color = player_colors[turn]
    # Transforming board position to pixel position
    x_pixel, y_pixel = get_pixel_pos_from_board_pos(board_x, board_y)
    # Draw hover only if the position is different from last hover
    if not last_hover \
            or last_hover[0] != x_pixel \
            or last_hover[1] != y_pixel:
        # Empties last hovered position
        delete_last_hover()
        # Draws a smaller circle at current cursor position on board
        pygame.draw.circle(game_screen,
                           color,
                           [x_pixel, y_pixel],
                           checker_hover_pixel_radius)
        last_hover = [x_pixel, y_pixel]
        pygame.display.update()
