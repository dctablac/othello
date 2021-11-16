# othello_logic.py
from collections import namedtuple

GameInfo = namedtuple('GameInfo', 'black_count '
                                  'white_count '
                                  'curr_turn '
                                  'winner '
                                  'is_game_over '
                                  'prev_move '
                                  'prev_turn')
Move = namedtuple('Move', 'row column')
Direction = namedtuple('Direction', 'NORTH SOUTH EAST WEST NORTHWEST NORTHEAST SOUTHEAST SOUTHWEST')

P_BLACK = 'B'
P_WHITE = 'W'
EMPTY_CELL = '-'
DIRECTION = Direction('north', 'south', 'east', 'west', 'northwest', 'northeast', 'southeast', 'southwest')


def default_game_info() -> namedtuple:
    """ Returns namedtuple of game info
        (black_count, white_count, curr_turn, winner, is_game_over, prev_move, prev_turn) """
    return GameInfo(2, 2, 'B', None, False, None, None)


def empty_game_board(n: int) -> [[str]]:
    """ Returns a nxn game board """
    board = []
    for i in range(n):
        row = ['-' for j in range(n)]
        board.append(row)
    _set_first_pieces(board)
    return board


def update_game_info(game_info: GameInfo, curr_move_row: int, curr_move_column: int,
                     new_black_count: int, new_white_count: int, winner=None, is_game_over=False) -> GameInfo:
    """ Returns updated game info """
    prev_move = Move(curr_move_row, curr_move_column)
    return game_info._replace(
        black_count=new_black_count,
        white_count=new_white_count,
        curr_turn=_change_turn(game_info.curr_turn),
        winner=winner,
        is_game_over=is_game_over,
        prev_move=prev_move,
        prev_turn=game_info.curr_turn
    )


def make_move(board: [[str]], move_row: int, move_column: int, curr_turn: str, flank_map: dict) -> [[str]]:
    """ Places a player piece on the board and flips opponent pieces that are outflanked. Returns new board. """
    # Place a player piece
    board = _place_piece_on_board(board, move_row, move_column, curr_turn)
    # Flip opponent pieces that are outflanked
    board = _flip_opponent_pieces(flank_map, board, move_row, move_column, curr_turn)
    return board


def count_player_pieces(board: [[str]], player: str) -> int:
    """ Counts the pieces of [player] on the board """
    if player != P_WHITE and player != P_BLACK:
        raise InvalidPlayerError('Player must be either B or W')
    count = 0
    for row in board:
        for col in row:
            if col == player:
                count += 1
    return count


# Validation functions


def is_valid_move(board: [[str]], row: int, column: int, curr_turn: str) -> (bool, dict):
    """ Validates a move. Valid if cell is within board indices, is empty, and an outflank is performable.
        Returns whether a move is valid and the dict of directions that can be flanked """
    board_len = len(board)
    if (row < 0 or row > board_len - 1) or (column < 0 or column > board_len - 1):
        raise InvalidMoveError
    if board[row][column] != EMPTY_CELL:
        raise InvalidMoveError
    flank_map = _create_flank_map(board, row, column, curr_turn)
    return _player_can_outflank(flank_map), flank_map


def is_valid_board_size(board_size: int) -> int:
    """ Validates the board size given """
    if board_size < 4 or board_size > 8 or (board_size % 2 != 0):
        return False
    return True


# Helper functions


def _set_first_pieces(board: [[str]]) -> [[str]]:
    """ Sets the initial pieces on the board """
    half_board_length = len(board) // 2
    board[half_board_length - 1][half_board_length - 1] = P_WHITE
    board[half_board_length][half_board_length] = P_WHITE
    board[half_board_length - 1][half_board_length] = P_BLACK
    board[half_board_length][half_board_length - 1] = P_BLACK
    return


def _change_turn(curr_turn: str) -> str:
    """ Changes the game turn """
    return P_WHITE if curr_turn == P_BLACK else P_BLACK


def _place_piece_on_board(board: [[str]], row: int, column: int, player: str) -> [[str]]:
    """ Places a piece on the game board """
    board[row][column] = player
    return board


def _create_flank_map(board: [[str]], move_row: int, move_column: int, player: str) -> {str: bool}:
    """ Creates a dictionary {direction, _can_outflank} that stores whether a move will outflank
        opponent pieces in a direction """
    position = Move(move_row, move_column)
    outflanking_directions = {DIRECTION.SOUTH: _can_outflank_south(board, position, player),
                              DIRECTION.NORTH: _can_outflank_north(board, position, player),
                              DIRECTION.EAST: _can_outflank_east(board, position, player),
                              DIRECTION.WEST: _can_outflank_west(board, position, player),
                              DIRECTION.SOUTHEAST: _can_outflank_southeast(board, position, player),
                              DIRECTION.SOUTHWEST: _can_outflank_southwest(board, position, player),
                              DIRECTION.NORTHEAST: _can_outflank_northeast(board, position, player),
                              DIRECTION.NORTHWEST: _can_outflank_northwest(board, position, player)}
    return outflanking_directions


def _flip_opponent_pieces(flank_map: dict, board: [[str]], move_row: int, move_column: int, player: str) -> [[str]]:
    """ Call all outflank functions in valid directions """
    position = Move(move_row, move_column)
    outflank_functions = {DIRECTION.SOUTH: _outflank_south,
                          DIRECTION.NORTH: _outflank_north,
                          DIRECTION.EAST: _outflank_east,
                          DIRECTION.WEST: _outflank_west,
                          DIRECTION.SOUTHEAST: _outflank_southeast,
                          DIRECTION.SOUTHWEST: _outflank_southwest,
                          DIRECTION.NORTHEAST: _outflank_northeast,
                          DIRECTION.NORTHWEST: _outflank_northwest}
    for direction in flank_map.keys():
        if flank_map[direction]:
            board = outflank_functions[direction](board, position, player)
    return board


def _player_can_outflank(flank_map: dict) -> bool:
    """ Verify if outflank is available in at least one direction """
    for direction in flank_map.keys():
        if flank_map[direction]:
            return True
    return False


# Functions to check and perform outflanks


def _can_outflank_south(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip south of current position """
    if not _boundary_check(DIRECTION.SOUTH, player_position, board):  # Needs to be third from last row minimum
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    for row_index in range(player_position.row + 1, len(board)):  # Check all rows after current row
        curr_position = board[row_index][player_position.column]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen  # True if opponent seen before player.
    return False  # # Reaches here if opponent piece encountered but flank not met by another player piece


def _can_outflank_north(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip north of current position """
    if not _boundary_check(DIRECTION.NORTH, player_position, board):  # Minimum third row from top
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    for row_index in range(player_position.row - 1, -1, -1):  # Check all rows before current row
        curr_position = board[row_index][player_position.column]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen  # True if opponent seen before player.
    return False  # Reaches here if opponent piece encountered but flank not met by another player piece


def _can_outflank_east(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip east of current position """
    if not _boundary_check(DIRECTION.EAST, player_position, board):  # Minimum third col from right
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    for col_index in range(player_position.column + 1, len(board)):  # Check all columns after current column
        curr_position = board[player_position.row][col_index]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen  # True if opponent seen before player.
    return False  # Reaches here if opponent piece encountered but flank not met by another player piece


def _can_outflank_west(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip west of current position """
    if not _boundary_check(DIRECTION.WEST, player_position, board):  # Minimum third col from left
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    for col_index in range(player_position.column - 1, -1, -1):  # Check all columns before current column
        curr_position = board[player_position.row][col_index]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen  # True if opponent seen before player.
    return False  # Reaches here if opponent piece encountered but flank not met by another player piece


def _can_outflank_southeast(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip southeast of current position """
    if not _boundary_check(DIRECTION.SOUTHEAST, player_position, board):  # Min third cell from lower right corner
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    col_index = player_position.column
    for row_index in range(player_position.row + 1, len(board)):
        col_index += 1
        curr_position = board[row_index][col_index]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen
    return False


def _can_outflank_southwest(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip southwest of current position """
    if not _boundary_check(DIRECTION.SOUTHWEST, player_position, board):
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    col_index = player_position.column
    for row_index in range(player_position.row + 1, len(board)):
        col_index -= 1
        curr_position = board[row_index][col_index]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen
    return False


def _can_outflank_northeast(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip northeast of current position """
    if not _boundary_check(DIRECTION.NORTHEAST, player_position, board):
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    col_index = player_position.column
    for row_index in range(player_position.row - 1, -1, -1):
        col_index += 1
        curr_position = board[row_index][col_index]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen
    return False


def _can_outflank_northwest(board: [[str]], player_position: Move, player: str) -> bool:
    """ Check if pieces will flip northwest of current position """
    if not _boundary_check(DIRECTION.NORTHWEST, player_position, board):
        return False
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    opponent_seen = False
    col_index = player_position.column
    for row_index in range(player_position.row - 1, -1, -1):
        col_index -= 1
        curr_position = board[row_index][col_index]
        if curr_position == EMPTY_CELL:
            return False
        if curr_position == opponent:
            opponent_seen = True
        elif curr_position == player:
            return opponent_seen
    return False


def _boundary_check(direction: str, position: Move, board: [[str]]) -> bool:
    """ Returns whether an outflank in a direction even has enough cells to take place """
    if direction == DIRECTION.SOUTH:
        return position.row < len(board) - 2
    elif direction == DIRECTION.NORTH:
        return position.row > 1
    elif direction == DIRECTION.EAST:
        return position.column < len(board) - 2
    elif direction == DIRECTION.WEST:
        return position.column > 1
    elif direction == DIRECTION.SOUTHEAST:
        return (position.row < len(board) - 2) and (position.column < len(board) - 2)
    elif direction == DIRECTION.SOUTHWEST:
        return (position.row < len(board) - 2) and (position.column > 1)
    elif direction == DIRECTION.NORTHEAST:
        return (position.row > 1) and (position.column < len(board) - 2)
    elif direction == DIRECTION.NORTHWEST:
        return (position.row > 1) and (position.column > 1)
    else:
        raise InvalidDirectionError


def _outflank_south(board: [[str]], player_position: Move, player: str) -> [[str]]:  # Return new board
    """ Flips pieces south of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    for row_index in range(player_position.row + 1, len(board)):  # Must stop when end player piece reached
        curr_position = board[row_index][player_position.column]
        if curr_position == opponent:
            board[row_index][player_position.column] = player
        else:
            return board


def _outflank_north(board: [[str]], player_position: Move, player: str) -> [[str]]:
    """ Flips pieces north of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    for row_index in range(player_position.row - 1, -1, -1):
        curr_position = board[row_index][player_position.column]
        if curr_position == opponent:
            board[row_index][player_position.column] = player
        else:
            return board


def _outflank_east(board: [[str]], player_position: Move, player: str) -> [[str]]:
    """ Flips pieces east of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    for col_index in range(player_position.column + 1, len(board)):
        curr_position = board[player_position.row][col_index]
        if curr_position == opponent:
            board[player_position.row][col_index] = player
        else:
            return board


def _outflank_west(board: [[str]], player_position: Move, player: str) -> [[str]]:
    """ Flips pieces west of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    for col_index in range(player_position.column - 1, -1, -1):
        curr_position = board[player_position.row][col_index]
        if curr_position == opponent:
            board[player_position.row][col_index] = player
        else:
            return board


def _outflank_southeast(board: [[str]], player_position: Move, player: str) -> [[str]]:
    """ Flips pieces southeast of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    col_index = player_position.column
    for row_index in range(player_position.row + 1, len(board)):
        col_index += 1
        curr_position = board[row_index][col_index]
        if curr_position == opponent:
            board[row_index][col_index] = player
        else:
            return board


def _outflank_southwest(board: [[str]], player_position: Move, player: str) -> [[str]]:
    """ Flips pieces southwest of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    col_index = player_position.column
    for row_index in range(player_position.row + 1, len(board)):
        col_index -= 1
        curr_position = board[row_index][col_index]
        if curr_position == opponent:
            board[row_index][col_index] = player
        else:
            return board


def _outflank_northeast(board: [[str]], player_position: Move, player: str) -> [[str]]:
    """ Flips pieces northeast of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    col_index = player_position.column
    for row_index in range(player_position.row - 1, -1, -1):
        col_index += 1
        curr_position = board[row_index][col_index]
        if curr_position == opponent:
            board[row_index][col_index] = player
        else:
            return board


def _outflank_northwest(board: [[str]], player_position: Move, player: str) -> [[str]]:
    """ Flips pieces northwest of current position """
    opponent = P_WHITE if player == P_BLACK else P_BLACK
    col_index = player_position.column
    for row_index in range(player_position.row - 1, -1, -1):
        col_index -= 1
        curr_position = board[row_index][col_index]
        if curr_position == opponent:
            board[row_index][col_index] = player
        else:
            return board


# Exception classes


class InvalidPlayerError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class InvalidDirectionError(Exception):
    pass
