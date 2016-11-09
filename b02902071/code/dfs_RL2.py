import json
import numpy as np
from copy import copy
from tools.readQuesiontFile import readQuestionFile
from tools.structure import *
from tools.RL import *
from tools.checker import checkSolution
import datetime
from bfs_heuristic_RL import get_row_positions
from time import sleep

def run_regular(state):
    ret = rule_1_1(state)
    if not ret: return [False, "1_1"]
    ret = rule_1_2(state)
    if not ret: return [False, "1_2"]
    ret = rule_1_3(state)
    if not ret: return [False, "1_3"]
    ret = rule_1_4(state)
    if not ret: return [False, "1_4"]
    ret = rule_1_5(state)
    if not ret: return [False, "1_5"]
    ret = rule_2_1(state)
    if not ret: return [False, "2_1"]
    ret = rule_2_2(state)
    if not ret: return [False, "2_2"]
    ret = rule_2_3(state)
    if not ret: return [False, "2_3"]
    ret = rule_2_4(state)
    if not ret: return [False, "2_4"]
    ret = rule_3_1(state)
    if not ret: return [False, "3_1"]
    ret = rule_3_2(state)
    if not ret: return [False, "3_2"]
    ret = rule_3_3(state)
    if not ret: return [False, "3_3"]

    return (True, "")

def regular(state):
    ret = run_regular(state)
    if not ret[0]: return ret + ["AA"]
    fliplr(state)
    ret = run_regular(state)
    if not ret[0]: return ret + ["AB"]
    fliplr(state)

    tranposeSolutionState(state)

    ret = run_regular(state)
    if not ret[0]: return ret + ["BA"]
    fliplr(state)
    ret = run_regular(state)
    if not ret[0]: return ret + ["BB"]
    fliplr(state)

    tranposeSolutionState(state)

    return (True, "")

def dfs_search(state, d, dfs_route):

    while True:
        old_sol_matrix = copy.deepcopy(state.sol_matrix)
        old_row_run_matrix = copy.deepcopy(state.row_run_matrix)
        old_col_run_matrix = copy.deepcopy(state.col_run_matrix)
        try:
            ret = regular(state)
            if ret[0] == False:
                # print ret[1]
                # print state.sol_matrix
                return None
        except:
            return None
        if (old_sol_matrix == state.sol_matrix).all() and (old_row_run_matrix == state.row_run_matrix).all() and \
                (old_col_run_matrix == state.col_run_matrix).all():
            break
    if len(np.where(state.isfilled_matrix == False)[0]) == 0:
        state.sol_matrix = np.where(state.sol_matrix > 0, True, False)
        if checkSolution(state):
            return state
        else:
            return None
    else:
        row_branch = None
        for row_positons in dfs_route:
            if False in state.isfilled_matrix[row_positons[1]]:
                state.isfilled_matrix[row_positons[1]] = True
                row_branch = row_positons
                break

        if row_branch == None:
            return None

        for row in row_branch[2]:
            # Cut useless branch
            continue_flag = False
            for idx, val in enumerate(state.sol_matrix[row_branch[1]]):
                if val != 0 and val != row[idx]:
                    continue_flag = True
                    break
            if continue_flag == True:
                continue

            next_state = copy.deepcopy(state)
            next_state.sol_matrix[row_branch[1]] = row

            ret_state = dfs_search(next_state, d+1, dfs_route)
            if ret_state != None:
                return ret_state

    return None

def dfs_RL(problem):
    '''
    :param problem:
    :return: solution

    '''

    state = initializeSolutionState(problem)

    dfs_route = []
    for idx, row in enumerate(state.row_hint):
        row_positions = get_row_positions(row, state.n)
        if row_positions is not None:
            dfs_route.append((len(row_positions), idx, row_positions))
        else:
            solution = None
            return solution
    dfs_route = sorted(dfs_route)

    ret = dfs_search(state, 0, dfs_route)
    if ret != None:
        return ret
    return None



if __name__ == "__main__":
    time_used = []
    p_list = readQuestionFile('./tcga2016-question.txt')

    # dfs_RL(p_list[92])

    for i in xrange(0, len(p_list)):
        cur = datetime.datetime.utcnow()
        print "#", i
        s = dfs_RL(p_list[i])
        print s.sol_matrix
        time_used.append(datetime.datetime.utcnow() - cur)
        for i, t in enumerate(time_used):
            print i, t
        print "--\n\n"

