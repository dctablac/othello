# othello_interface.py
import othello_logic


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
    while True:  # Board size validation
        try:
            board_size = int(input('Board size [4, 6, or 8] (or 0 to quit): '))
            if board_size == 0:
                return  # Game exited
            if othello_logic.is_valid_board_size(board_size):
                break
            raise ValueError
        except ValueError:
            print('Please enter a board size of 4, 6, or 8')

    game_board = othello_logic.empty_game_board(board_size)
    game_info = othello_logic.default_game_info()
    error_msg = None

    while True:  # Main game loop
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
            is_valid_move, flank_map = othello_logic.is_valid_move(game_board, move_row,
                                                                   move_column, game_info.curr_turn)
            if is_valid_move:
                # Place player piece and flip opponent pieces
                game_board = othello_logic.make_move(game_board, move_row, move_column, game_info.curr_turn, flank_map)
                # Update game info with new piece counts
                black_count = othello_logic.count_player_pieces(game_board, othello_logic.P_BLACK)
                white_count = othello_logic.count_player_pieces(game_board, othello_logic.P_WHITE)
                game_info = othello_logic.update_game_info(game_info, move_row, move_column, black_count, white_count)
                error_msg = None
            else:
                raise othello_logic.InvalidMoveError
        except othello_logic.InvalidMoveError:
            error_msg = 'Invalid move.'
        except ValueError:
            error_msg = 'Please enter numbers in the range 0-9.'
        except IndexError:
            error_msg = 'Invalid move. Please enter a row number and a column number in the range 0-9.'
