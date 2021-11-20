import abc
import copy

import numpy as np
from typing import Optional, Literal
from connectfour_lib import evaluate_connect_four, is_game_won, move, undo_move
import copy

class GameState:
    @abc.abstractmethod
    def get_possible_moves(self, player):
        pass

    @abc.abstractmethod
    def move(self, player, move):
        pass

    @abc.abstractmethod
    def undo_move(self, player, move):
        pass

    @abc.abstractmethod
    def evaluate(self):
        pass

    @abc.abstractmethod
    def is_game_won(self):
        pass

    @abc.abstractmethod
    def get_hash(self):
        pass

class ConnectFourState(GameState):
    n_cols = 7
    n_rows = 6

    def __init__(self, state: Optional['ConnectFourState']=None):
        super().__init__()
        if state is None:
            self.state = np.zeros([self.n_rows, self.n_cols], dtype=np.int32)
        else:
            self.state = np.array(state.state, dtype=np.int32)

    def is_game_won(self):
        return is_game_won(self.state)

    def get_possible_moves(self, player):
        if self.is_game_won():
            return []
        else:
            return np.where(self.state[0] == 0)[0]
        # moves = []
        # if self.is_game_won() != 0:
        #     return moves
        # for col in range(self.n_cols):
        #     if self.state[0,col] == 0:
        #         for row in range(self.n_rows):
        #             if self.state[row, col] != 0:
        #                 row -= 1
        #                 break
        #         m = ConnectFourState(self)
        #         m.state[row, col] = player
        #         moves.append(m)
        # return moves

    def __str__(self):
        s = ""
        for row in self.state:
            s += "|"+"|".join([[" ", "x", "o"][p] for p in row]) + "|\n"
        s += "-" * (2*self.n_cols + 1) + "\n"
        s += "|" + "|".join([str(i) for i in range(self.n_cols)]) + "|\n"
        return s

    def _get_cols_of_length(self, n, player):
        other_player = 3 - player
        n_found = 0
        for row in range(self.n_rows-4):
            for col in range(self.n_cols):
                segment = self.state[row:row+4, col]
                if np.all(segment != other_player) and (np.sum(segment == player) == n):
                    n_found += 1
        return n_found

    def _get_rows_of_length(self, n, player):
        other_player = 3 - player
        n_found = 0
        for row in range(self.n_rows):
            for col in range(self.n_cols-4):
                segment = self.state[row, col:col+4]
                if np.all(segment != other_player) and (np.sum(segment == player) == n):
                    n_found += 1
        return n_found

    def _get_diag1_of_length(self, n, player):
        other_player = 3 - player
        n_found = 0
        for row in range(self.n_rows - 4):
            for col in range(self.n_cols-4):
                segment = self.state[row+np.arange(4), col+np.arange(4)]
                if np.all(segment != other_player) and (np.sum(segment == player) == n):
                    n_found += 1
        return n_found


    def _get_diag2_of_length(self, n, player):
        other_player = 3 - player
        n_found = 0
        for row in range(self.n_rows - 4):
            for col in range(4, self.n_cols):
                segment = self.state[row+np.arange(4), col-np.arange(4)]
                if np.all(segment != other_player) and (np.sum(segment == player) == n):
                    n_found += 1
        return n_found

    def _get_lines_of_length(self, n, player):
        return self._get_rows_of_length(n, player) + \
               self._get_cols_of_length(n, player) + \
               self._get_diag1_of_length(n, player) + \
               self._get_diag2_of_length(n, player)


    def move(self, player, col):
        return move(self.state, player, col)

    def undo_move(self, player, col):
        return undo_move(self.state, player, col)

    def evaluate(self):
        return evaluate_connect_four(self.state)

    def get_hash(self):
        return tuple(self.state.flatten())

cache_dict = dict()
def alpha_beta_pruning(state: GameState, depth: int, player: Literal[1,2], alpha=None, beta=None):
    if depth == 0:
        return state.evaluate(), None, 1
    hash_key = (state.get_hash(), depth, player)
    if hash_key in cache_dict:
        return cache_dict[hash_key] + (0,)

    alpha = alpha or -np.inf
    beta = beta or np.inf
    possible_moves = state.get_possible_moves(player)
    if len(possible_moves) == 0:
        return state.evaluate(), None, 1

    other_player = 3 - player
    maximize = (player == 1)

    best_move = None
    best_value = -np.inf if maximize else np.inf
    n_moves_evaluated = 0
    for move in possible_moves:
        state.move(player, move)
        if state.is_game_won() == player:
            best_value = 100_000 * (3 - 2*player)
            state.undo_move(player, move)
            cache_dict[hash_key] = (best_value, best_move)
            return best_value, move, 0
        value, _, sub_moves_evaluated = alpha_beta_pruning(state, depth-1, other_player, alpha, beta)
        state.undo_move(player, move)
        n_moves_evaluated += sub_moves_evaluated
        if maximize:
            if value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, value)
            if value >= beta:
                break
        else:
            if value < best_value:
                best_value = value
                best_move = move
                beta = min(beta, value)
            if value <= alpha:
                break

    cache_dict[hash_key] = (best_value, best_move)
    return best_value, best_move, n_moves_evaluated



if __name__ == '__main__':
    s = ConnectFourState()
    depth = 10


    while True:
        print(s)
        valid_move = False
        while not valid_move:
            p1_choice = int(input(f"Which move [0-{s.n_cols}]? "))
            # _, p1_choice, _ = alpha_beta_pruning(s, depth, 1)
            # p1_choice = np.random.randint(s.n_cols)
            valid_move = s.move(1, p1_choice)
        if s.is_game_won():
            print(s)
            print("Game over. You won!")
            break

        estimated_value, p2_choice, n_evals = alpha_beta_pruning(s, depth, 2)
        s.move(2, p2_choice)
        print(f"{n_evals} moves evaluated: Estimated value = {estimated_value}")
        if s.is_game_won():
            print(s)
            print("Game over. Computer won!")
            break

