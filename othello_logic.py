# othello_logic.py
from collections import namedtuple

GameInfo = namedtuple('GameInfo', 'black_count white_count curr_turn winner is_game_over prev_turn prev_move')
Move = namedtuple('Move', 'row column')


def default_game_info() -> namedtuple:
    """ Returns namedtuple of game info
        (black_count, white_count, turn, winner, is_game_over, prev_turn, prev_move) """
    return GameInfo(2, 2, 'B', None, False, None, None)


def set_game_board(n: int) -> [[str]]:
    """ Returns a nxn game board """
    board = []
    for i in range(n):
        row = ['-' for j in range(n)]
        board.append(row)
    _set_first_pieces(board)
    return board


def _set_first_pieces(board: [[str]]) -> [[str]]:
    """ Sets the initial pieces on the board """
    half_board_length = len(board) // 2
    board[half_board_length - 1][half_board_length - 1] = 'W'
    board[half_board_length][half_board_length] = 'W'
    board[half_board_length - 1][half_board_length] = 'B'
    board[half_board_length][half_board_length - 1] = 'B'
    return


def place_piece_on_board(board: [[str]], row: int, column: int, turn: str) -> [[str]]:
    """ Places a piece on the game board """
    board[row][column] = turn
    return board


def flip_valid_pieces(board: [[str]], recent_move: str) -> [[str]]:
    """ Flips pieces according the most recent move made """
    pass


# Validation functions

def is_valid_move(board: [[str]], row: int, column: int) -> bool:
    """ Validates a move """
    # Accept moves as row, col or (row, col)
    if board[row][column] != '-':
        return False
    return True
