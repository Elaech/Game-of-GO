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
stone_count = None


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
    global stone_count
    empty_checker = -1
    player1_checker = 0
    player2_checker = 1
    scores = [0, 0]
    stone_count = [0, 0]
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


def is_suicidal_move(board_x, board_y, turn):
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


def find_other_turn_neighbours(board_x, board_y):
    turn_queue = [[board_x, board_y]]
    other_queue = []
    index = 0
    max_index = 0
    while index <= max_index:
        pos = turn_queue[index]
        for moves in neighbours:
            new_x = pos[0] + moves[0]
            new_y = pos[1] + moves[1]
            if valid_position(new_x, new_y):
                if table[new_x][new_y] == turn and [new_x, new_y] not in turn_queue:
                    turn_queue.append([new_x, new_y])
                    max_index += 1
                elif table[new_x][new_y] == get_other_turn() and [new_x, new_y] not in other_queue:
                    other_queue.append([new_x, new_y])

        index += 1
    return other_queue


def is_capturing_move(board_x, board_y):
    neighbouring_border = find_other_turn_neighbours(board_x, board_y)
    index = 0
    max_index = len(neighbouring_border) - 1
    while index <= max_index:
        pos = neighbouring_border[index]
        for moves in neighbours:
            new_x = pos[0] + moves[0]
            new_y = pos[1] + moves[1]
            if valid_position(new_x, new_y):
                if table[new_x][new_y] == get_other_turn() \
                        and [new_x, new_y] not in neighbouring_border:
                    neighbouring_border.append([new_x, new_y])
                    max_index += 1
                elif table[new_x][new_y] == empty_checker \
                        and (new_x != board_x or new_y != board_y):
                    return False, []
        index += 1
    return True, neighbouring_border


def find_other_turn_immediate_neighbours(board_x, board_y):
    immediate_neighbours = []
    for moves in neighbours:
        new_x = board_x + moves[0]
        new_y = board_y + moves[1]
        if valid_position(new_x, new_y) and table[new_x][new_y] == get_other_turn():
            immediate_neighbours.append([new_x, new_y])
    return immediate_neighbours


def get_encircled(board_x, board_y):
    immediate_neighbours = find_other_turn_immediate_neighbours(board_x, board_y)
    encircled_territory = []
    for position in immediate_neighbours:
        if position not in encircled_territory:
            local_territory = [position]
            index = 0
            max_index = 0
            captured = True
            while index <= max_index:
                pos = local_territory[index]
                for moves in neighbours:
                    new_x = pos[0] + moves[0]
                    new_y = pos[1] + moves[1]
                    if valid_position(new_x, new_y):
                        if table[new_x][new_y] == get_other_turn() \
                                and [new_x, new_y] not in local_territory:
                            local_territory.append([new_x, new_y])
                            max_index += 1
                        elif table[new_x][new_y] == empty_checker \
                                and (new_x != board_x or new_y != board_y):
                            captured = False
                index += 1
            if captured:
                encircled_territory.extend(local_territory)
    return (len(encircled_territory) != 0), encircled_territory


def is_ko(board_x, board_y):
    if kos[turn]:
        return kos[turn][0] == board_x and kos[turn][1] == board_y
    return False


def is_legal_move(board_x, board_y):
    empty = table[board_x][board_y] == empty_checker
    suicidal = is_suicidal_move(board_x, board_y, turn)
    captures, captured_territory = is_capturing_move(board_x, board_y)
    if not captures:
        captures, captured_territory = get_encircled(board_x, board_y)
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
    else:
        for board_x in range(len(table)):
            for board_y in range(len(table[0])):
                if is_legal_move(board_x, board_y):
                    return False
        return True


def player_pass():
    global passes
    passes[turn] = True
    change_turn()


def explore_territory(board_x, board_y):
    local_territory = [[board_x, board_y]]
    player1_pieces = []
    player2_pieces = []
    index = 0
    max_index = 0
    is_player1_margin = False
    is_player2_margin = False
    while index <= max_index:
        pos = local_territory[index]
        for moves in neighbours:
            new_x = pos[0] + moves[0]
            new_y = pos[1] + moves[1]
            if valid_position(new_x, new_y):
                if table[new_x][new_y] == empty_checker \
                        and [new_x, new_y] not in local_territory:
                    local_territory.append([new_x, new_y])
                    max_index += 1
                elif table[new_x][new_y] == player1_checker:
                    is_player1_margin = True
                    player1_pieces.extend([new_x, new_y])
                elif table[new_x][new_y] == player2_checker:
                    is_player2_margin = True
                    player2_pieces.extend([new_x, new_y])
        index += 1

    owner = -1
    if is_player2_margin and not is_player1_margin:
        owner = player2_checker
    elif is_player1_margin and not is_player2_margin:
        owner = player1_checker
    return local_territory, owner


def calculate_territory():
    visited = []
    local_scores = [0, 0]
    for index_x in range(len(table)):
        for index_y in range(len(table[0])):
            if table[index_x][index_y] == empty_checker \
                    and [index_x, index_y] not in visited:
                territory, owner = explore_territory(index_x, index_y)
                visited.extend(territory)
                if owner == player1_checker:
                    local_scores[0] += len(territory)
                elif owner == player2_checker:
                    local_scores[1] += len(territory)
    return local_scores


def update_scores():
    global scores
    territory_scores = calculate_territory()
    scores[0] = stone_count[0] + territory_scores[0]
    scores[1] = stone_count[1] + territory_scores[1]


def update_kos(captured_territory):
    global kos
    ko_add = None
    ko_remove = None
    if kos[get_other_turn()]:
        ko_remove = kos[get_other_turn()]
        kos[get_other_turn()] = None
    if len(captured_territory) == 1:
        ko_add = captured_territory[0]
        kos[get_other_turn()] = captured_territory[0]
    return ko_add, ko_remove


def capture_territory(board_x, board_y):
    global stone_count
    global table
    table[board_x][board_y] = turn
    stone_count[turn] += 1
    capturing, captured_territory = is_capturing_move(board_x, board_y)
    if not capturing:
        capturing, captured_territory = get_encircled(board_x, board_y)
    stone_count[get_other_turn()] -= len(captured_territory)
    for position in captured_territory:
        table[position[0]][position[1]] = empty_checker
    return captured_territory


def move(board_x, board_y):
    global passes
    passes = [False, False]
    captured_territory = capture_territory(board_x, board_y)
    update_scores()
    ko_add, ko_remove = update_kos(captured_territory)
    return captured_territory, ko_add, ko_remove


def change_turn():
    global turn
    if turn == player1_checker:
        turn = player2_checker
    else:
        turn = player1_checker


def get_turn():
    return turn


def get_other_turn():
    if turn == player1_checker:
        return player2_checker
    else:
        return player1_checker


def get_player_checker(player_nr):
    checkers = [None, player1_checker, player2_checker]
    return checkers[player_nr]
