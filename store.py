# For storing the game states.

import errors


class GameStore(object):
    def __init__(self):
        self.games = {}

    def get_games(self):
        return self.games.values()

    def get_game(self, game_id):
        return self.games.get(game_id)

    def add_game(self, game):
        if game.id in self.games.keys():
            return (False, errors.already_exists_error)
        self.games[game.id] = game
        return (True, '')

    def update_game(self, game_id, game):
        if game_id not in self.games.keys():
            return (False, errors.not_found_error)
        self.games[game_id] = game
        return (True, '')

    def delete_game(self, game_id):
        if game_id not in self.games.keys():
            return (False, errors.not_found_error)
        del self.games[game_id]
        return (True, '')


store_instance = GameStore()
