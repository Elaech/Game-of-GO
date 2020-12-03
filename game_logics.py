"""
This is the logical module for the project Game-of-GO
It contains methods that handle the board and score of the game
"""

# Variables that are used globally by this module
table = None  # Contains the board of the game
turn = None  # Contains the current player turn
empty_checker = None  # Contains the emtpy board space
player1_checker = None
player2_checker = None
scores = None
kos = None  # Contains the current positions for the KOs
neighbours = [[1, 0], [-1, 0], [0, 1], [0, -1]]
board_size = None
passes = None  # Contains the current passing situation for the game
stone_count = None  # Contains the curret stone count for each player


def get_scores():
    """
    Returns player scores
    :return: 1st player score, 2nd player score
    """
    return scores[0], scores[1]


def initialise_game(options):
    """
    Initialises all the global variables that are needed in game logic
    and the representative values of players, checkers, empty spaces etc
    Initialises and Fills the entire board with empty spaces
    Initialises the variables that help calculating the scores
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
    """
    Checks if a position is located on the board
    :param board_x: x coordinate
    :param board_y: y coordinate
    :return: True or False
    """
    return 0 <= board_y < board_size \
           and 0 <= board_x < board_size


def is_suicidal_move(board_x, board_y, turn):
    """
    Checks if a move is suicidal for a player
    A move is suicidal if (after making it) a stone/group of stones of the player associated with turn
    is surrounded by enemy stones
    The strategy is followed is flooding to see if we can find an empty checker nearby
    :param board_x: x coordinate
    :param board_y: y coordinate
    :param turn: Player for which to check
    :return: True or False
    """
    queue = [[board_x, board_y]]
    index = 0
    max_index = 0
    # Checking all passable space
    while index <= max_index:
        pos = queue[index]
        for moves in neighbours:
            new_x = pos[0] + moves[0]
            new_y = pos[1] + moves[1]
            if valid_position(new_x, new_y) \
                    and [new_x, new_y] not in queue:
                # Appending same player checkers positions
                if table[new_x][new_y] == turn:
                    queue.append([new_x, new_y])
                    max_index += 1
                # Stopping if group is not surrounded
                elif table[new_x][new_y] == empty_checker:
                    return False
        index += 1
    return True


def find_other_turn_neighbours(board_x, board_y):
    """
    Returns the enemy neighbours of the friendly group in which the move is placed
    Floods the friendly neighboring space and saves any enemy checker found along the way
    :param board_x: x coordinate
    :param board_y: y  coordinate
    :return: list of position tuples with enemy neighbours of the friendly group
    """
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
                # Moving on friendly group
                if table[new_x][new_y] == turn \
                        and [new_x, new_y] not in turn_queue:
                    turn_queue.append([new_x, new_y])
                    max_index += 1
                # Saving enemy found checkers along the way
                elif table[new_x][new_y] == get_other_turn() \
                        and [new_x, new_y] not in other_queue:
                    other_queue.append([new_x, new_y])
        index += 1
    return other_queue


def is_capturing_move(board_x, board_y):
    """
    Checks if the neighboring enemy border is surrounded by a friendly boarder
    if it is then it can be captured,
    else it cannot and will have at least one liberty
    It also returns a list containing the captured checkers/stones, if any exist
    :param board_x: x coordinate of the move
    :param board_y: y coordinate of the move
    :return: (False,[]) OR (True, a list  of the enemy boarder positions that are captured)
    """
    neighbouring_border = find_other_turn_neighbours(board_x,
                                                     board_y)
    index = 0
    max_index = len(neighbouring_border) - 1
    while index <= max_index:
        pos = neighbouring_border[index]
        for moves in neighbours:
            new_x = pos[0] + moves[0]
            new_y = pos[1] + moves[1]
            if valid_position(new_x, new_y):
                # Advancing on enemy boarder
                if table[new_x][new_y] == get_other_turn() \
                        and [new_x, new_y] not in neighbouring_border:
                    neighbouring_border.append([new_x, new_y])
                    max_index += 1
                # If we find a liberty
                elif table[new_x][new_y] == empty_checker \
                        and (new_x != board_x or new_y != board_y):
                    return False, []
        index += 1
    return True, neighbouring_border


def find_other_turn_immediate_neighbours(board_x, board_y):
    """
    Finds the enemy stones surrounding an empty position
    :param board_x: x coordinate
    :param board_y: y coordinate
    :return: list of enemy neighbours surrounding the position given
    """
    immediate_neighbours = []
    # Going through immediate vicinity
    for moves in neighbours:
        new_x = board_x + moves[0]
        new_y = board_y + moves[1]
        # Getting valid enemy stone positions
        if valid_position(new_x, new_y) \
                and table[new_x][new_y] == get_other_turn():
            immediate_neighbours.append([new_x, new_y])
    return immediate_neighbours


def is_encircling_move(board_x, board_y):
    """
    Checks if (by making the given move for the current player on the table)
    the current player captures an enemy group by surrounding it
    Analyzing the immediate neighbouring enemy groups we can decide if any/all of them
    are surrounded after making the move
    If any of the groups are surrounded it returns a list containing their positions
    :param board_x: x coordinate of the move
    :param board_y: y coordinate of the move
    :return: (False,[]) or (True, list of captured enemy stones positions)
    """
    immediate_neighbours = find_other_turn_immediate_neighbours(board_x,
                                                                board_y)
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
    """
    Checks if a position is blocked by the KO rule for the current player
    :param board_x: x coordinate
    :param board_y: y coordinate
    :return: True or False
    """
    if kos[turn]:
        return kos[turn][0] == board_x \
               and kos[turn][1] == board_y
    return False


def is_legal_move(board_x, board_y):
    """
    Tests if a given move can be played by the current player
    by testing different conditions for the GO game:
    1. The move must be made on an empty space
    2. The move cannot be just a simple suicidal move
    3. If the move is suicidal it must also capture enemy territory
    3.INFO. Capturing enemy territory can be done by encircling
     or by filling and encircling the enemy territory aat the same time
    :param board_x: x coordinate
    :param board_y: y coordinate
    :return: True or False
    """
    empty = table[board_x][board_y] == empty_checker
    suicidal = is_suicidal_move(board_x,
                                board_y,
                                turn)
    captures, captured_territory = is_capturing_move(board_x,
                                                     board_y)
    if not captures:
        captures, captured_territory = is_encircling_move(board_x,
                                                          board_y)
    ko = is_ko(board_x, board_y)
    return empty and (not suicidal or (suicidal and captures)) and not ko


def game_is_finished():
    """
    Checks to see if the game is finished according to the GO rules.
    1.A game is finished is both players pass
    OR 2. A game is finished if the current player cannot make a legal move on the board
    :return: True or False
    """
    if passes[0] and passes[1]:
        return True
    else:
        for board_x in range(len(table)):
            for board_y in range(len(table[0])):
                if is_legal_move(board_x, board_y):
                    return False
        return True


def player_pass():
    """
    Passes current player turn, marking it accordingly
    :return: None
    """
    global passes
    passes[turn] = True
    change_turn()


def explore_territory(board_x, board_y):
    """
    Explores empty territory starting from a given board position
    While exploring it takes into account which player stones are surrounding it
    The player surrounding it is the owner
    If both players or no players are surrounding the territory then it has no owner yet
    :param board_x: x coordinate
    :param board_y: y coordinate
    :return: list of positions of local territory, owner of the territory
    """
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
                # Exploring empty spaces
                if table[new_x][new_y] == empty_checker \
                        and [new_x, new_y] not in local_territory:
                    local_territory.append([new_x, new_y])
                    max_index += 1
                # Completing player 1 margin
                elif table[new_x][new_y] == player1_checker:
                    is_player1_margin = True
                    player1_pieces.extend([new_x, new_y])
                # Completing player 2 margin
                elif table[new_x][new_y] == player2_checker:
                    is_player2_margin = True
                    player2_pieces.extend([new_x, new_y])
        index += 1

    owner = -1
    # Checking whose territory is the one identified
    if is_player2_margin\
            and not is_player1_margin:
        owner = player2_checker
    elif is_player1_margin\
            and not is_player2_margin:
        owner = player1_checker
    return local_territory, owner


def calculate_territory():
    """
    Going through each territory on the board
    if it is owned by any player => we add the area of the territory to that player's score
    if it is not owned we ignore it
    :return: list containing territory score for each player
    """
    visited = []
    territory_scores = [0, 0]  # contains the territory scores for each player
    for index_x in range(len(table)):
        for index_y in range(len(table[0])):
            # if the current position is not part of an already explored territory
            if table[index_x][index_y] == empty_checker \
                    and [index_x, index_y] not in visited:
                # Explore territory
                territory, owner = explore_territory(index_x,
                                                     index_y)
                visited.extend(territory)
                # Adding the territory points if it has an owner
                if owner == player1_checker:
                    territory_scores[0] += len(territory)
                elif owner == player2_checker:
                    territory_scores[1] += len(territory)
    return territory_scores


def update_scores():
    """
    Updates player scores using one of the GO rules for updating scores:
    player score = area of territory + number of own stones
    :return: None
    """
    global scores
    territory_scores = calculate_territory()
    scores[0] = stone_count[0] + territory_scores[0]
    scores[1] = stone_count[1] + territory_scores[1]


def update_kos(captured_territory):
    """
    Updates the current KOs on the board according to the GO rules.
    A KO is a move that cannot be played by its corresponding player
    and it appears for the enemy when the current player captures only 1 enemy stone
    at the captured stone position
    :param captured_territory: list of positions being the territory being captured
    :return: position for adding KO, position for removing KO
    """
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
    """
    When a player makes a move it has the following effects on the board:
    1. Captures the position given
    2. If the move captures a group of enemy stones, the enemy stones are removed
    :param board_x:  x coordinate of the move
    :param board_y: y coordinate of the move
    :return: list containing the positions of the captured territory
    """
    global table
    table[board_x][board_y] = turn
    stone_count[turn] += 1
    capturing, captured_territory = is_capturing_move(board_x,
                                                      board_y)
    if not capturing:
        capturing, captured_territory = is_encircling_move(board_x,
                                                           board_y)
    for position in captured_territory:
        table[position[0]][position[1]] = empty_checker
    return captured_territory


def move(board_x, board_y):
    """
    Makes the move provided for the current player
    Modifies the table and score according to the move and its captured territories
    :param board_x: x coordinate of the move
    :param board_y: y coordinate of the move
    :return: list containing positions of captured territory, None or new KO position, None or old KO position
    """
    global stone_count
    global passes
    passes = [False, False]
    # Captured territory
    captured_territory = capture_territory(board_x,
                                           board_y)
    # Removing the captured territory from the enemy score
    stone_count[get_other_turn()] -= len(captured_territory)
    # Updating the score
    update_scores()
    # Updating the KO positions
    ko_add, ko_remove = update_kos(captured_territory)
    return captured_territory, ko_add, ko_remove


def change_turn():
    """
    Changes the turn between player 1 and player 2 alternatively
    :return: None
    """
    global turn
    if turn == player1_checker:
        turn = player2_checker
    else:
        turn = player1_checker


def get_turn():
    """
    :return: current player turn
    """
    return turn


def get_other_turn():
    """
    :return: not current player turn
    """
    if turn == player1_checker:
        return player2_checker
    else:
        return player1_checker


def get_player_checker(player_nr):
    """
    :param player_nr: "1" - player1, "2" - player2
    :return: corresponding checker for the player given
    """
    checkers = [None, player1_checker, player2_checker]
    return checkers[player_nr]


def get_board_size():
    return board_size
