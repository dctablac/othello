# othello_logic.py
from collections import namedtuple

GameInfo = namedtuple('GameInfo', 'black_count white_count curr_turn winner is_game_over prev_move prev_turn')
Move = namedtuple('Move', 'row column')

P_BLACK = 'B'
P_WHITE = 'W'


def default_game_info() -> namedtuple:
    """ Returns namedtuple of game info
        (black_count, white_count, curr_turn, winner, is_game_over, prev_move, prev_turn) """
    return GameInfo(2, 2, 'B', None, False, None, None)


def set_game_board(n: int) -> [[str]]:
    """ Returns a nxn game board """
    board = []
    for i in range(n):
        row = ['-' for j in range(n)]
        board.append(row)
    _set_first_pieces(board)
    return board


def place_piece_on_board(board: [[str]], row: int, column: int, turn: str) -> [[str]]:
    """ Places a piece on the game board """
    board[row][column] = turn
    return board


def flip_valid_pieces(board: [[str]], recent_move: str) -> [[str]]:
    """ Flips pieces according the most recent move made """
    pass


def update_game_info(game_info: GameInfo, curr_move_row: int, curr_move_column: int,
                     new_black_count: int, new_white_count: int, winner=None, is_game_over=False) -> GameInfo:
    """ Returns update game info """
    prev_move = Move(curr_move_row, curr_move_column);
    return game_info._replace(
        black_count=new_black_count,
        white_count=new_white_count,
        curr_turn=_flip_turn(game_info.curr_turn),
        winner=winner,
        is_game_over=is_game_over,
        prev_move=prev_move,
        prev_turn=game_info.curr_turn
    )


def count_player_pieces(board: [[str]], player: str) -> int:
    """ Counts the pieces of [player] on the board"""
    if player != P_WHITE and player != P_BLACK:
        raise InvalidPlayerError('Player must be either B or W')
    count = 0
    for row in board:
        for col in row:
            if col == player:
                count += 1
    return count


# Helper functions


def _set_first_pieces(board: [[str]]) -> [[str]]:
    """ Sets the initial pieces on the board """
    half_board_length = len(board) // 2
    board[half_board_length - 1][half_board_length - 1] = P_WHITE
    board[half_board_length][half_board_length] = P_WHITE
    board[half_board_length - 1][half_board_length] = P_BLACK
    board[half_board_length][half_board_length - 1] = P_BLACK
    return


def _flip_turn(turn: str) -> str:
    """ Flips the game turn """
    return P_WHITE if turn == P_BLACK else P_BLACK


# Validation functions


def is_valid_move(board: [[str]], row: int, column: int) -> bool:
    """ Validates a move """
    board_len = len(board)
    if (row < 0 or row > board_len - 1) or (column < 0 or column > board_len - 1):
        raise InvalidMoveError
    if board[row][column] != '-':
        raise InvalidMoveError
    # TODO: Extra checks
    return True


# Exception classes


class InvalidPlayerError(Exception):
    pass


class InvalidMoveError(Exception):
    pass
