table = None
turn = None
empty_checker = None
player1_checker = None
player2_checker = None
player1_score = None
player2_score = None
player1_ko = None
player2_ko = None
error_message = None

def get_scores():
    return player1_score, player2_score


def initialise_game(options):
    """
    Initialises all the global variables that are needed for in game logic
    and the representative values of players, checkers, empty spaces etc
    Initialises and Fills the entire board with empty spaces
    Initialises the player scores
    :param options: variables that are needed in order to start the game logic, received from the controller
    """
    global empty_checker
    global player1_score
    global player2_score
    global player1_checker
    global player2_checker
    global turn
    global table
    empty_checker = -1
    player1_checker = 0
    player2_checker = 1
    player1_score = 0
    player2_score = 0
    turn = player1_checker
    table = []
    for column_index in range(options["board-size"]):
        line = []
        for row_index in range(options["board-size"]):
            line.append(-1)
        table.append(line)


def is_legal_move(x, y):
    return table[x][y] == -1


def show_table():
    for line in table:
        print(line)


def move(board_x, board_y):
    table[board_x][board_y] = turn


def change_turn():
    global turn
    if turn == player1_checker:
        turn = player2_checker
    else:
        turn = player1_checker


def get_turn():
    return turn
