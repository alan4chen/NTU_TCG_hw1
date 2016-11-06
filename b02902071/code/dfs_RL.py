import json
import numpy as np
from copy import copy
from tools.readQuesiontFile import readQuestionFile
from tools.structure import *
from tools.RL import *
from tools.checker import checkSolution
import datetime
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

def dfs_search(state, d):

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
        unknown_cells = np.where(state.sol_matrix == 0)
        if d == 0:
            print state.sol_matrix

        for cell in zip(unknown_cells[0], unknown_cells[1]):
            next_state = copy.deepcopy(state)
            next_state.sol_matrix[cell[0]][cell[1]] = 1
            # next_state.sol_matrix[cell[0]][1] = -1
            # next_state.sol_matrix[cell[0]][2] = -1
            # print "d:", d
            # print next_state.sol_matrix
            ret_state = dfs_search(next_state, d+1)
            if ret_state != None:
                return ret_state

            next_state = copy.deepcopy(state)
            next_state.sol_matrix[cell[0]][cell[1]] = -1
            ret_state = dfs_search(next_state, d + 1)
            if ret_state != None:
                return ret_state

    return None

def dfs_RL(problem):
    '''
    :param problem:
    :return: solution

    '''

    state = initializeSolutionState(problem)
    # print state.row_run

    # for i in range(0, 50):
    #     # print "--"
    #     assert rule_1_1(state)
    #     assert rule_1_2(state)
    #     assert rule_1_3(state)
    #     assert rule_1_4(state)
    #     assert rule_1_5(state)
    #     assert rule_2_1(state)
    #     assert rule_2_2(state)
    #     assert rule_2_3(state)
    #     assert rule_2_4(state)
    #     assert rule_3_1(state)
    #     assert rule_3_2(state)
    #     # print state.row_run_matrix[7][7]
    #     assert rule_3_3(state)
    #     # print state.row_run_matrix[7][7]
    #     tranposeSolutionState(state)
    #     assert rule_1_1(state)
    #     assert rule_1_2(state)
    #     assert rule_1_3(state)
    #     assert rule_1_4(state)
    #     assert rule_1_5(state)
    #     assert rule_2_1(state)
    #     assert rule_2_2(state)
    #     assert rule_2_3(state)
    #     assert rule_2_4(state)
    #     assert rule_3_1(state)
    #     assert rule_3_2(state)
    #     assert rule_3_3(state)
    #     tranposeSolutionState(state)

    ret = dfs_search(state, 0)
    if ret != None:
        # ret.sol_matrix = np.where(ret.sol_matrix > 0, True, False)
        # if not checkSolution(ret):
        #     print ret.sol_matrix
        #     print "BUG!!"
        #     raise()
        print ret.sol_matrix
    print "\n"


if __name__ == "__main__":
    time_used = []
    p_list = readQuestionFile('./tcga2016-question.txt')

    # dfs_RL(p_list[92])

    for i in xrange(0, len(p_list)):
        cur = datetime.datetime.utcnow()
        print "#", i
        dfs_RL(p_list[i])
        print datetime.datetime.utcnow() - cur
        time_used.append(datetime.datetime.utcnow() - cur)
        print "--\n\n"

    for i, t in enumerate(time_used):
        print i, t
    # for idx, p in enumerate(p_list):
    #     s = dfs_RL(p)
    #     if s is not None:
    #         print s.sol_matrix
    #     else:
    #         print "Warning! NO SOLUTION!!"
    #         print "idx: ", idx
    #         exit()
    #     print "--"