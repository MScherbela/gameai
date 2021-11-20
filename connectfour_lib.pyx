import numpy as np

cdef _get_cols_of_length(int[:,:] state, int n, int player):
    cdef int other_player = 3 - player
    cdef int n_found = 0
    cdef Py_ssize_t row
    cdef Py_ssize_t col
    cdef Py_ssize_t offset
    cdef int count

    for row in range(state.shape[0]-3):
        for col in range(state.shape[1]):
            count = 0
            for offset in range(4):
                if state[row+offset, col] == other_player:
                    count = 0
                    break
                elif state[row+offset, col] == player:
                    count += 1
            if count >= n:
                n_found += 1
    return n_found

cdef _get_rows_of_length(int[:,:] state, int n, int player):
    cdef int other_player = 3 - player
    cdef int n_found = 0
    cdef Py_ssize_t row
    cdef Py_ssize_t col
    cdef Py_ssize_t offset
    cdef int count

    for row in range(state.shape[0]):
        for col in range(state.shape[1]-3):
            count = 0
            for offset in range(4):
                if state[row, col+offset] == other_player:
                    count = 0
                    break
                elif state[row, col+offset] == player:
                    count += 1
            if count >= n:
                n_found += 1
    return n_found

cdef _get_diag1_of_length(int[:,:] state, int n, int player):
    cdef int other_player = 3 - player
    cdef int n_found = 0
    cdef Py_ssize_t row
    cdef Py_ssize_t col
    cdef Py_ssize_t offset
    cdef int count

    for row in range(state.shape[0]-3):
        for col in range(state.shape[1]-3):
            count = 0
            for offset in range(4):
                if state[row+offset, col+offset] == other_player:
                    count = 0
                    break
                elif state[row+offset, col+offset] == player:
                    count += 1
            if count >= n:
                n_found += 1
    return n_found

cdef _get_diag2_of_length(int[:,:] state, int n, int player):
    cdef int other_player = 3 - player
    cdef int n_found = 0
    cdef Py_ssize_t row
    cdef Py_ssize_t col
    cdef Py_ssize_t offset
    cdef int count

    for row in range(state.shape[0]-4):
        for col in range(3, state.shape[1]):
            count = 0
            for offset in range(4):
                if state[row+offset, col-offset] == other_player:
                    count = 0
                    break
                elif state[row+offset, col-offset] == player:
                    count += 1
            if count >= n:
                n_found += 1
    return n_found


cdef _get_lines_of_length(int[:,:] state, int n, int player):
    return _get_rows_of_length(state, n, player) + \
           _get_cols_of_length(state, n, player) + \
           _get_diag1_of_length(state, n, player) + \
           _get_diag2_of_length(state, n, player)

def evaluate_connect_four(int[:,:] state, float weight_3 = 10.0, float weight_4 = 100000.0):
    cdef int i
    cdef float estimated_value = 0.0
    for i in range(2):
        player = i + 1
        sign = 1 - 2*i
        estimated_value += sign * _get_lines_of_length(state, 3, player) * weight_3
        estimated_value += sign * _get_lines_of_length(state, 4, player) * weight_4
    return estimated_value

def is_game_won(int[:,:] state):
    cdef int player
    for player in range(1,3):
        if _get_lines_of_length(state, 4, player) > 0:
            return player
    return 0

def move(int[:,:] state, int player, int col):
    cdef Py_ssize_t row
    if state[0,col] != 0:
        return False
    for row in range(state.shape[0]-1, -1, -1):
        if state[row, col] == 0:
            state[row, col] = player
            break
    return True

def undo_move(int[:,:] state, int player, int col):
    cdef Py_ssize_t row
    for row in range(state.shape[0]):
        if state[row, col] != 0:
            state[row, col] = 0
            break



