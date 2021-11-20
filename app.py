from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import json
import othello_logic

app = Flask(__name__)

@app.route('/game/new_game', methods=['POST'])
def get_info():
    # Returns a blank board (based on board size) and game info
    board_size = int(request.json['boardSize'])
    
    data = json.dumps({ 'board': othello_logic.empty_game_board(board_size), 'game_info': othello_logic.default_game_info() })
    response = make_response(data)
    response.content_type = 'application/json'

    return response

@app.route('/game/update_info', methods=['POST'])
def update_game():
    # Makes move if acceptable and returns updated board and game info, else return error msg
    board = request.board
    game_info = request.game_info
    move_row, move_column = request.move_row, request.move_column

    is_valid_move, flank_map = othello_logic.is_valid_move(board, move_row, move_column, game_info.curr_turn)

    data = json.dumps({ 'board': board, 'game_info': game_info })
    response = make_response(data)
    response.content_type = 'application/json'

    return response


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
