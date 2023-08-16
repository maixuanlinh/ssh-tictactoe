# python3

from flask import (Flask, request, make_response, render_template)

import game
import errors
from store import store_instance


app = Flask('ssh-test-application')

from flask import Flask, request, make_response, jsonify
import game
import errors

app = Flask(__name__)

@app.route('/api/v1/games', methods=['GET', 'POST'])
def games():
    print("Handling request for /api/v1/games...")  # Log entry point

    if request.method == 'GET':
        print("Processing GET request...")
        json_games = [g.get_json() for g in store_instance.get_games()]
        print(f"Found {len(json_games)} games.")  # Log the number of games found
        return make_response({'games': json_games})

    if request.method == 'POST':
        print("Processing POST request...")

        if request.is_json:
            board = request.get_json().get('board')
            print(f"Received board: {board}")  # Log the board received
        else:
            print("Error: Request is not JSON format.")
            return make_response({'error': 'Invalid request'}, 400)

        game_obj = game.Game()
        ok, error = game_obj.update_board(board)
        if not ok:
            print(f"Error updating board: {error}")  # Log error encountered
            return make_response(
                {'error': error},
                errors.get_error_code(error))

        ok, error = store_instance.add_game(game_obj)
        if not ok:
            print(f"Error adding game to store: {error}")  # Log error encountered
            return make_response(
                {'error': error},
                errors.get_error_code(error))

        print(f"Game created successfully with id: {game_obj.id}")  # Log the game's ID
        resp = make_response(game_obj.get_json(), 201)
        resp.headers['Location'] = 'api/vi/games/' + game_obj.id
        return resp

    print("Error: Method not allowed.")  # Log error for methods not 'GET' or 'POST'
    return make_response(
        {'error': errors.method_not_allowed},
        errors.get_error_code(errors.method_not_allowed))



@app.route('/api/v1/games/<game_id>', methods=['GET', 'PUT', 'DELETE'])
def game_id(game_id):
    if request.method == 'GET':
        game_obj = store_instance.get_game(game_id)
        if game_obj is None:
            return make_response(
                {'error': errors.not_found_error},
                errors.get_error_code(errors.not_found_error))
        return make_response(game_obj.get_json())

    if request.method == 'PUT':
        if request.is_json:
            board = request.get_json().get('board')
        else:
            return make_response({'error': 'Invalid request'}, 400)

        game_obj = store_instance.get_game(game_id)
        if game_obj is None:
            return make_response(
                {'error': errors.not_found_error},
                errors.get_error_code(errors.not_found_error))

        if game_obj.is_finished():
            return make_response(
                {'error': errors.game_finished},
                errors.get_error_code(errors.game_finished))

        ok, error = game_obj.update_board(board)
        if not ok:
            return make_response(
                {'error': error},
                errors.get_error_code(error))

        ok, error = store_instance.update_game(game_id, game_obj)
        if not ok:
            return make_response(
                {'error': error},
                errors.get_error_code(error))

        return make_response(game_obj.get_json())

    if request.method == 'DELETE':
        ok, error = store_instance.delete_game(game_id)
        if not ok:
            return make_response(
                {'error': error},
                errors.get_error_code(error))

        return make_response({})

    return make_response({'error': 'Method not allowed'}, 405)

# Route to serve the main game interface - the index.html
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
