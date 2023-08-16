import requests
import random

ADDRESS = 'http://127.0.0.1:5555/api/v1/games'
MY_MARK = 'x'


def list_games():
    response = requests.get(ADDRESS)
    print(response.json())


def get_game_by_id(game_id):
    response = requests.get('{}/{}'.format(ADDRESS, game_id))
    return response.json()


def create_game():
    headers = {'Content-Type': 'application/json;'}
    response = requests.post(
        ADDRESS,
        json={'board': '----{}----'.format(MY_MARK)},
        headers=headers)
    return response.json()['id']


def create_game_opponent_start():
    headers = {'Content-Type': 'application/json;'}
    response = requests.post(
        ADDRESS,
        json={'board': '---------'},
        headers=headers)
    return response.json()['id']


def update_game(game_obj):
    headers = {'Content-Type': 'application/json;'}
    response = requests.put(
        '{}/{}'.format(ADDRESS, game_obj['id']),
        json={'board': game_obj['board']},
        headers=headers)
    if response.status_code != 200:
        print(response.json())


def remove_game(game_id):
    response = requests.delete('{}/{}'.format(ADDRESS, game_id))


def make_random_move(game_obj, mymark=MY_MARK):
    empty_slots = []
    for index, mark in enumerate(game_obj['board']):
        if mark not in ['x', 'o']:
            empty_slots.append(index)

    if empty_slots:
        slot = random.choice(empty_slots)
        tmp_board = list(game_obj['board'])
        tmp_board[slot] = mymark
        game_obj['board'] = ''.join(tmp_board)

    update_game(game_obj)


def run():
    print('CREATE SOME GAMES')
    game_id = create_game()
    game_id2 = create_game_opponent_start()
    list_games()

    print('GET GAME AND PLAY SOME')
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)
    make_random_move(game_obj)
    game_obj = get_game_by_id(game_id)
    print(game_obj)

    print('GET GAME AND PLAY SOME')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)
    make_random_move(game_obj, 'o')
    game_obj = get_game_by_id(game_id2)
    print(game_obj)

    print('LIST GAMES AND DELETE A GAME')
    list_games()
    remove_game(game_id2)
    list_games()


if __name__ == '__main__':
    run()
