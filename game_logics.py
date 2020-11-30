table = None
turn = None
empty_checker = None
player1_checker = None
player2_checker = None
scores = None
kos = None
error_message = None
neighbours = [[1, 0], [-1, 0], [0, 1], [0, -1]]
board_size = None
passes = None


def get_scores():
    return scores[0], scores[1]


def initialise_game(options):
    """
    Initialises all the global variables that are needed for in game logic
    and the representative values of players, checkers, empty spaces etc
    Initialises and Fills the entire board with empty spaces
    Initialises the player scores
    :param options: variables that are needed in order to start the game logic, received from the controller
    """
    global empty_checker
    global scores
    global kos
    global player1_checker
    global player2_checker
    global turn
    global table
    global passes
    global board_size
    empty_checker = -1
    player1_checker = 0
    player2_checker = 1
    scores = [0, 0]
    kos = [None, None]
    turn = player1_checker
    board_size = options["board-size"]
    table = []
    passes = [False, False]
    for column_index in range(board_size):
        line = []
        for row_index in range(board_size):
            line.append(-1)
        table.append(line)


def valid_position(board_x, board_y):
    return 0 <= board_y < board_size \
           and 0 <= board_x < board_size


def is_suicidal_move(board_x, board_y):
    queue = [[board_x, board_y]]
    index = 0
    max_index = 0
    while index <= max_index:
        pos = queue[index]
        for moves in neighbours:
            new_x = pos[0] + moves[0]
            new_y = pos[1] + moves[1]
            if valid_position(new_x, new_y) and [new_x, new_y] not in queue:
                if table[new_x][new_y] == turn:
                    queue.append([new_x, new_y])
                    max_index += 1
                elif table[new_x][new_y] == empty_checker:
                    return False
        index += 1
    return True


def is_capturing_move(board_x, board_y):
    pass


def is_ko(board_x, board_y):
    if kos[turn]:
        return kos[turn][0] == board_x and kos[turn][1] == board_y
    return False


def update_scores():
    pass


def is_legal_move(board_x, board_y):
    empty = table[board_x][board_y] == empty_checker
    suicidal = is_suicidal_move(board_x, board_y)
    captures = is_capturing_move(board_x, board_y)
    ko = is_ko(board_x, board_y)
    return empty \
           and (not suicidal or (suicidal and captures)) \
           and not ko


def show_table():
    for line in table:
        print(line)


def game_is_finished():
    if passes[0] and passes[1]:
        return True


def player_pass():
    global passes
    passes[turn] = True
    change_turn()


def move(board_x, board_y):
    global passes
    passes = [False, False]
    table[board_x][board_y] = turn


def change_turn():
    global turn
    if turn == player1_checker:
        turn = player2_checker
    else:
        turn = player1_checker


def get_turn():
    return turn


def get_player_checker(player_nr):
    checkers = [None, player1_checker, player2_checker]
    return checkers[player_nr]
