# The game objects and logic.

import uuid
import random
import json
import errors


GAME_STATUSES = [
    'RUNNING',
    'X_WON',
    'O_WON',
    'DRAW',
]

CROSS = 'x'
NOUGHT = 'o'
MARKS = [
    CROSS,
    NOUGHT,
]

EMPTY_BOARD = '-' * 9

WIN_CONDITIONS = [
    # horizontal
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),

    # vertical
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),

    # corners
    (0, 4, 8),
    (2, 4, 6),
]


class Game(object):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.board = EMPTY_BOARD
        self.status = 'RUNNING'

        self._player = ''
        self._opponent = ''
        self._first_player = ''

    def _valid_move(self, board):
        # values are sensible
        if len(board) > len(EMPTY_BOARD):
            return (False, errors.invalid_value)
        if (board.count(CROSS) + board.count(NOUGHT) +
                board.count('-')) < len(EMPTY_BOARD):
            return (False, errors.invalid_value)

        # can't overwrite existing positions
        for index, mark in enumerate(board):
            if mark in MARKS:
                current = self.board[index]
                if current in MARKS and current != mark:
                    return (False, errors.invalid_value)

        # is it correct turn
        if self._first_player == 'PLAYER':
            if board.count(self._player) - board.count(self._opponent) != 1:
                return (False, errors.invalid_value)
        else:
            if board.count(self._opponent) - board.count(self._player) != 0:
                return (False, errors.invalid_value)

        return (True, '')

    def _make_opponent_move(self):
        # Opponent makes a random move.
        empty_slots = []
        for index, mark in enumerate(self.board):
            if mark not in MARKS:
                empty_slots.append(index)

        if empty_slots:
            slot = random.choice(empty_slots)
            tmp_board = list(self.board)
            tmp_board[slot] = self._opponent
            self.board = ''.join(tmp_board)

    def _check_winning_conditions(self):
        # Check if someone won the game.

        if self.board.count('-') == 0:
            # No moves left
            self.status = 'DRAW'
            return

        board = list(self.board)
        for cond in WIN_CONDITIONS:
            marks = []
            for index in cond:
                mark = board[index]
                if mark in MARKS:
                    marks.append(mark)
            if len(marks) == 3 and len(set(marks)) == 1:
                # someone won!
                if set(marks).pop() == CROSS:
                    self.status = 'X_WON'
                else:
                    self.status = 'O_WON'
                break

    def get_json(self):
        return json.dumps(
            {'id': self.id,
             'board': self.board,
             'status': self.status})

    def _start_new_game(self, board):
        if board == EMPTY_BOARD:
            # Computer moves first and chooses crosses.
            self._first_player = 'COMP'
            self._opponent = CROSS
            self._player = NOUGHT
        else:
            # Player moves first
            self._first_player = 'PLAYER'
            if board.count(CROSS) + board.count(NOUGHT) != 1:
                return (False, errors.invalid_value)

            mark = board.strip('-')
            if mark not in MARKS:
                return (False, errors.invalid_value)

            self._player = mark
            tmp = list(MARKS)
            tmp.remove(self._player)
            self._opponent = tmp[0]

        return (True, '')

    def update_board(self, board):
        if self.board == EMPTY_BOARD:
            # New game requested
            ok, error = self._start_new_game(board)
            if not ok:
                return (False, error)
            if self._first_player == 'COMP':
                self._make_opponent_move()
                return (True, '')

        if self.is_finished():
            return (False, errors.game_finished)

        valid, error = self._valid_move(board)
        if not valid:
            return (False, error)

        self.board = board
        self._check_winning_conditions()

        if not self.is_finished():
            self._make_opponent_move()
            self._check_winning_conditions()

        return (True, '')

    def is_finished(self):
        return self.status != 'RUNNING'
