import pygame
import pygame.freetype

board_size = None
board_pixel_size = None
board_size = None
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


def initialise_game(options):
    """
    Initialises all globals that are needed for drawing anything on the user interface
    The values for initialisation are received from the controller
    It also creates the game screen on which all the elements are drawn
    :param options: information from the controller concerning pixels, sizes, fonts, colors
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
    global line_thickness
    global valid_color
    global invalid_color
    board_size = options["board-size"]
    checker_pixel_size = options["checker-pixel-size"]
    board_pixel_size = (board_size + 1) * checker_pixel_size
    line_color = options["line-color"]
    invalid_color = options["invalid-color"]
    score_pixel_size = options["score-pixel-size"]
    font = pygame.freetype.SysFont("Arial", score_pixel_size / 2)
    upper_board_margin = checker_pixel_size
    lower_board_margin = checker_pixel_size * board_size
    background_color = options["background-color"]
    player_colors = options["player-colors"]
    line_thickness = options["line-thickness"]
    game_screen = pygame.display.set_mode((board_pixel_size, board_pixel_size + score_pixel_size))


def draw_initial_board():
    """
    Draws the initial board of the game of GO on the user interface
    All the values respect the initialisation
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


def draw_scores(player1_score, player2_score, move_error=None):
    """
    Draws the score part of the user interface along with the eventual errors of attempted moves
    This part is visibile under the board and it consists in 3 parts: player1score, player2score, and error_msg
    :param player1_score: current player1 score
    :param player2_score: current player2 score
    :param move_error: if the last move produced an error this contains the err_string
    """
    pygame.draw.rect(game_screen,
                     background_color,
                     [0,board_pixel_size,board_pixel_size,board_pixel_size+score_pixel_size])
    padding = score_pixel_size / 8
    pygame.draw.rect(game_screen,
                     player_colors[0],
                     [padding, board_pixel_size - padding, score_pixel_size * 2.5, score_pixel_size - padding],
                     line_thickness)
    pygame.draw.rect(game_screen,
                     player_colors[1],
                     [score_pixel_size * 2.5 + padding * 2, board_pixel_size - padding, score_pixel_size * 2.5,
                      score_pixel_size - padding],
                     line_thickness)
    font.render_to(game_screen,
                   (padding * 2, board_pixel_size + padding),
                   "Player1: " + str(player1_score),
                   player_colors[0])
    font.render_to(game_screen,
                   (score_pixel_size * 2.5 + padding * 4, board_pixel_size + padding),
                   "Player2: " + str(player2_score),
                   player_colors[1])
    if move_error:
        font.render_to(game_screen,
                       (score_pixel_size * 5 + padding * 4, board_pixel_size + padding),
                       move_error,
                       invalid_color)
    pygame.display.update()


def draw_checker(color, x, y):
    pass


def draw_position_hover():
    pass


def draw_empty(x, y):
    pass


def draw_ko_block():
    pass


def draw_winner(message):
    pass
