# othello_interface.py
import othello_logic


def validate_board_size() -> int:
    """ Validates the board size given or quits the game """
    while True:
        try:
            board_size = input('Board size [4, 6, or 8] (or "quit" to quit): ')
            if board_size == 'quit':
                return -1
            board_size = int(board_size)
            if board_size < 4 or board_size > 8 or (board_size % 2 != 0):
                raise ValueError
            return board_size
        except ValueError:
            print('Please enter a board size of 4, 6, or 8')


def print_board(board: [[str]]) -> None:
    """ Prints the game board to the console """
    # Column indices
    print('\n')
    print('  ', end='')
    for col_index in range(len(board)):  # board has equal column to row
        print(f' {col_index} ', end='')
    print('\n')
    for row_index in range(len(board)):
        print(f'{row_index} ', end='')  # Row index
        for col in board[row_index]:
            print(f' {col} ', end='')
        print('\n')
    return


def game_loop():
    """ Runs the game loop """
    print('#----------OTHELLO----------#')
    board_size = validate_board_size()
    if board_size == -1:
        return
    game_board = othello_logic.set_game_board(board_size)
    game_info = othello_logic.default_game_info()
    error_msg = None

    while True:
        print('#----------#')
        print_board(game_board)
        print(f'\nB: {game_info.black_count} | ', end='')
        print(f'W: {game_info.white_count}')
        if error_msg is not None:
            print(error_msg)
        if game_info.prev_turn is not None and error_msg is None:
            print(f'Placed {game_info.prev_turn} at ({game_info.prev_move.row},{game_info.prev_move.column})')
        print(f'Turn: {game_info.curr_turn}')
        move = input('Please enter a move: [row] [col] (or "quit" to quit)\n')
        if move == 'quit':
            return print('Game quit. Game over!')
        try:
            move = move.split(' ')
            move_row, move_column = int(move[0]), int(move[1])
            if othello_logic.is_valid_move(game_board, move_row, move_column):
                game_board = othello_logic.place_piece_on_board(game_board, move_row, move_column, game_info.curr_turn)
                black_count = othello_logic.count_player_pieces(game_board, othello_logic.P_BLACK)
                white_count = othello_logic.count_player_pieces(game_board, othello_logic.P_WHITE)
                game_info = othello_logic.update_game_info(game_info, move_row, move_column, black_count, white_count)
                error_msg = None
            else:
                raise othello_logic.InvalidMoveError
        except othello_logic.InvalidMoveError:
            error_msg = 'Invalid move.'
        except ValueError:
            error_msg = "Invalid move. Please enter numbers in range 0-9"
