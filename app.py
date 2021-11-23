from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import json
import othello_logic

app = Flask(__name__)

@app.route('/game/new_game', methods=['POST'])
def get_info():
    ''' Route for getting a blank board and game info '''
    # Returns a blank board (based on board size) and game info
    board_size = int(request.json['boardSize'])
    
    data = json.dumps({ 'board': othello_logic.empty_game_board(board_size), 'game_info': othello_logic.default_game_info() })
    response = make_response(data)
    response.content_type = 'application/json'

    return response

@app.route('/game/request_move', methods=['POST'])
def update_game():
    ''' Route for making a move and updating the game state '''
    # Makes move if acceptable and returns updated board and game info, else return error msg
    req_body = request.json
    board = req_body['board']
    game_info = othello_logic.GameInfo._make(req_body['game_info']) # Parse array into game_info namedtuple
    move_row, move_column = int(req_body['move_row']), int(req_body['move_column'])

    try:
        is_valid_move, flank_map = othello_logic.is_valid_move(board, move_row, move_column, game_info.curr_turn)
        if is_valid_move:
            board = othello_logic.make_move(board, move_row, move_column, game_info.curr_turn, flank_map)
            count_black = othello_logic.count_player_pieces(board, othello_logic.P_BLACK)
            count_white = othello_logic.count_player_pieces(board, othello_logic.P_WHITE)
            game_info = othello_logic.update_game_info(game_info, move_row, move_column, 
                                                    count_black, count_white)
            if othello_logic.is_game_over(board) is False:
                data = json.dumps({ 
                    'board': board, 
                    'game_info': game_info, 
                    'message': 'Move accepted', 
                    'status': 200 
                })
            else:
                data = json.dumps({
                    'board': board,
                    'game_info': game_info,
                    'message': 'Game over',
                    'status': 201,
                    'winner': othello_logic.P_BLACK if count_black > count_white else othello_logic.P_WHITE
                })
        else:
            data = json.dumps({ 
                'board': board, 
                'game_info': game_info, 
                'message': 'Invalid move', 
                'status': 500 
            })
    except othello_logic.InvalidMoveError:
        data = json.dumps({ 
            'board': board, 
            'game_info': game_info, 
            'message': 'Invalid move', 
            'status': 500 
        })
    finally:
        response = make_response(data)
        response.content_type = 'application/json'
        return response

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
