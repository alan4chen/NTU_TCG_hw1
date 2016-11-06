import numpy as np
from RL_tools import *
import copy


class Stack:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items) - 1]
    def size(self):
        return len(self.items)


class Solution:
    sol_matrix = None
    n = 0
    row_hint = None
    col_hint = None

class Problem:
    n = 0
    row_hint = None
    col_hint = None
    hint_content = None
    def __init__(self):
        Problem.hint_content=[]


class SolutionState:
    sol_matrix = None
    isfilled_matrix = None
    row_run_matrix = None
    col_run_matrix = None
    n = 0
    row_hint = None
    col_hint = None
    row_run = None
    col_run = None
    transpose = False
    flip = False

def tranposeSolutionState(state):
    state.transpose = not state.transpose
    state.row_hint, state.col_hint = state.col_hint, state.row_hint
    state.row_run, state.col_run = state.col_run, state.row_run
    state.sol_matrix = np.transpose(state.sol_matrix)
    state.isfilled_matrix = np.transpose(state.isfilled_matrix)
    state.row_run_matrix, state.col_run_matrix = state.col_run_matrix, state.row_run_matrix
    return state

def fliplr(state):
    state.flip = not state.flip
    state.sol_matrix = np.fliplr(state.sol_matrix)
    state.isfilled_matrix = np.fliplr(state.isfilled_matrix)
    for i in xrange(0, state.n):
        state.row_hint[i] = state.row_hint[i][::-1]
    for i in xrange(0, state.n):
        state.row_run[i] = state.row_run[i][::-1]
        for j in xrange(0, len(state.row_run[i])):
            n_list = []
            n_list.append(state.n - 1 - state.row_run[i][j][1])
            n_list.append(state.n - 1 - state.row_run[i][j][0])
            state.row_run[i][j] = n_list
        updateRunMatrix(state, i)

def initializeSolutionState(problem):
    def initializeRun(state):
        for index, rowHint in enumerate(state.row_hint):
            run_list = []
            for idx in xrange(0, len(rowHint)):
                run_list.append([0,0])
                if idx == 0:
                    run_list[idx][0] = 0
                else:
                    run_list[idx][0] = sum(rowHint[0:idx]) + len(rowHint[0:idx])
                if idx == len(rowHint)-1:
                    run_list[idx][1] = state.n - 1
                else:
                    run_list[idx][1] = state.n - 1 - sum(rowHint[idx+1:]) - len(rowHint[idx+1:])
                for i in range(run_list[idx][0], run_list[idx][1]+1):
                    state.row_run_matrix[index][i].append(idx)
            state.row_run.append(run_list)
        return

    state = SolutionState()
    state.n = problem.n
    state.row_hint = problem.row_hint
    state.col_hint = problem.col_hint
    state.row_run_matrix = np.empty((state.n, state.n), dtype=object)
    for i in range(0, state.n):
        for j in range(0, state.n):
            state.row_run_matrix[i][j] = []
    state.col_run_matrix = copy.deepcopy(state.row_run_matrix)
    state.sol_matrix = np.zeros((state.n, state.n), dtype='int8')
    state.isfilled_matrix = np.zeros((state.n, state.n), dtype='bool')
    state.row_run = []
    state.col_run = []
    initializeRun(state)
    state = tranposeSolutionState(state)
    initializeRun(state)
    state = tranposeSolutionState(state)
    return state


if __name__ == "__main__":

    # test initializeSolutionState
    p = Problem()
    p.n = 3
    p.row_hint = [[1,1],[1],[2]]
    p.col_hint = [[1],[2],[1,1]]
    state = initializeSolutionState(p)
    assert state.row_run == [[[0, 0], [2, 2]], [[0, 2]], [[0, 2]]]
    assert state.col_run == [[[0, 2]], [[0, 2]], [[0, 0], [2, 2]]]


    p = Problem()
    p.n = 4
    p.row_hint = [[1], [1], [3], [1]]
    p.col_hint = [[1], [2], [1, 2], []]
    state = initializeSolutionState(p)
    assert state.row_run == [[[0, 3]], [[0, 3]], [[0, 3]], [[0, 3]]]
    assert state.col_run == [[[0, 3]], [[0, 3]], [[0, 0], [2, 3]], []]

    # test flippr
    p = Problem()
    p.n = 4
    p.row_hint = [[1], [1], [3], [1]]
    p.col_hint = [[1], [2], [1, 2], []]
    state = initializeSolutionState(p)
    fliplr(state)
    assert state.row_run == [[[0, 3]], [[0, 3]], [[0, 3]], [[0, 3]]]

    p = Problem()
    p.n = 3
    p.row_hint = [[1, 1], [1], [2]]
    p.col_hint = [[1], [2], [1, 1]]
    state = initializeSolutionState(p)
    fliplr(state)
    print state.row_run
    assert state.row_run == [[[0, 0], [2, 2]], [[0, 2]], [[0, 2]]]





