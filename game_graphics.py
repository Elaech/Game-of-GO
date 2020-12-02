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
last_hover = None
checker_hover_pixel_radius = None
checker_pixel_radius = None
ko_pixel_length = None
score_padding = None


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
    font = pygame.freetype.SysFont("Arial", score_pixel_size / 2)
    upper_board_margin = checker_pixel_size
    lower_board_margin = checker_pixel_size * board_size
    background_color = options["background-color"]
    player_colors = options["player-colors"]
    line_thickness = options["line-thickness"]
    score_padding = score_pixel_size / 8
    ko_pixel_length = checker_pixel_size / 3
    checker_hover_pixel_radius = checker_pixel_size / 3
    checker_pixel_radius = checker_pixel_size / 2 - 2
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


def draw_scores(player1_score, player2_score):
    """
    Draws the score part of the user interface along with the eventual errors of attempted moves
    This part is visibile under the board and it consists in 3 parts: player1score, player2score, and error_msg
    :param player1_score: current player1 score
    :param player2_score: current player2 score
    :param move_error: if the last move produced an error this contains the err_string
    """
    pygame.draw.rect(game_screen,
                     background_color,
                     [0, board_pixel_size, board_pixel_size, board_pixel_size + score_pixel_size])
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
    pygame.draw.rect(game_screen,
                     background_color,
                     [score_pixel_size * 5 + score_padding * 4, board_pixel_size + score_padding, board_pixel_size,
                      board_pixel_size + score_pixel_size])
    if error:
        font.render_to(game_screen,
                       (score_pixel_size * 5 + score_padding * 4, board_pixel_size + score_padding),
                       message,
                       invalid_color)
    else:
        font.render_to(game_screen,
                       (score_pixel_size * 5 + score_padding * 4, board_pixel_size + score_padding),
                       message,
                       valid_color)
    pygame.display.update()


def draw_stone(turn, board_x, board_y):
    color = player_colors[turn]
    x_pixel, y_pixel = get_pixel_pos_from_board_pos(board_x, board_y)
    pygame.draw.circle(game_screen, color, [x_pixel, y_pixel], checker_pixel_radius)
    pygame.display.update()


def delete_stone(board_x, board_y):
    pixel_x,pixel_y = get_pixel_pos_from_board_pos(board_x,board_y)
    draw_empty_pixel_pos(pixel_x,pixel_y)


def draw_empty_pixel_pos(x_pixel, y_pixel):
    pygame.draw.circle(game_screen,
                       background_color,
                       [x_pixel, y_pixel],
                       checker_pixel_radius)
    north = max(y_pixel - checker_pixel_radius, checker_pixel_size)
    south = min(y_pixel + checker_pixel_radius, board_pixel_size - checker_pixel_size)
    east = max(x_pixel - checker_pixel_radius, checker_pixel_size)
    west = min(x_pixel + checker_pixel_radius, board_pixel_size - checker_pixel_size)
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
    color = player_colors[turn]
    x_pixel, y_pixel = get_pixel_pos_from_board_pos(board_x, board_y)
    pygame.draw.rect(game_screen,
                     color,
                     [x_pixel - ko_pixel_length, y_pixel - ko_pixel_length, 2 * ko_pixel_length, 2 * ko_pixel_length],
                     line_thickness)
    pygame.display.update()


def get_board_position(mouse_x, mouse_y):
    x_pos = int((mouse_x - checker_pixel_size / 2) / checker_pixel_size)
    y_pos = int((mouse_y - checker_pixel_size / 2) / checker_pixel_size)
    return x_pos, y_pos


def get_pixel_pos_from_board_pos(board_x, board_y):
    x_pos = board_x * checker_pixel_size + checker_pixel_size
    y_pos = board_y * checker_pixel_size + checker_pixel_size
    return x_pos, y_pos


def mouse_on_board(mouse_x, mouse_y):
    return board_pixel_size - checker_pixel_size / 2 > mouse_y > checker_pixel_size / 2 \
           and checker_pixel_size / 2 < mouse_x < board_pixel_size - checker_pixel_size / 2


def get_pixel_board_position(mouse_x, mouse_y):
    x_pos = int((mouse_x + checker_pixel_size / 2) / checker_pixel_size) * checker_pixel_size
    y_pos = int((mouse_y + checker_pixel_size / 2) / checker_pixel_size) * checker_pixel_size
    return x_pos, y_pos


def delete_last_hover():
    global last_hover
    if last_hover:
        draw_empty_pixel_pos(last_hover[0], last_hover[1])
    last_hover = None


def draw_mouse_hover(turn, board_x, board_y):
    global last_hover
    color = player_colors[turn]
    x_pixel, y_pixel = get_pixel_pos_from_board_pos(board_x, board_y)
    if not last_hover or last_hover[0] != x_pixel or last_hover[1] != y_pixel:
        delete_last_hover()
        pygame.draw.circle(game_screen, color, [x_pixel, y_pixel], checker_hover_pixel_radius)
        last_hover = [x_pixel, y_pixel]
        pygame.display.update()
