import json
import numpy as np
from copy import copy
import cPickle
import hashlib
from tools.readQuesiontFile import readQuestionFile
from tools.structure import *
from tools.RL import *
from tools.checker import checkSolution
import datetime
from tools.compositions import compositions
from Queue import PriorityQueue
from collections import Counter
from time import sleep
import settings
from collections import defaultdict

def get_row_positions(row_hint, n):
    if len(row_hint) == 0:
        return [[-1] * n]
    if sum(row_hint) + len(row_hint) - 1 > n:
        return None
    positions = []
    zero_n = n - sum(row_hint) - len(row_hint) + 1
    for zero_add in compositions(zero_n, len(row_hint)+1):
        ret = []
        iter_zero_add = iter(zero_add)
        iter_hint = iter(row_hint)
        ret += [-1] * next(iter_zero_add)
        ret += [1] * next(iter_hint)
        for i in xrange(0, len(row_hint)-1):
            ret += [-1]
            ret += [-1] * next(iter_zero_add)
            ret += [1] * next(iter_hint)
        ret += [-1] * next(iter_zero_add)
        positions.append(ret)
    return positions

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
    if not ret:
        return [False, "3_3"]
    return (True, "")

def regular(state):
    ret = run_regular(state)
    if not ret[0]: return ret + ["AA"]
    fliplr(state)
    ret = run_regular(state)
    if not ret[0]:
        return ret + ["AB"]
    fliplr(state)

    tranposeSolutionState(state)
    ret = run_regular(state)
    if not ret[0]:
        return ret + ["BA"]
    fliplr(state)
    ret = run_regular(state)
    if not ret[0]:
        return ret + ["BB"]
    fliplr(state)

    tranposeSolutionState(state)

    return (True, "")


def fit_regular(state):
    m = hashlib.md5()
    m.update(cPickle.dumps(state))
    old_hash = m.digest()
    while True:
        try:
            ret = regular(state)
        except:
            return False
        if ret[0] == False:
            # print state.sol_matrix
            return False
        m.update(cPickle.dumps(state))
        new_hash = m.digest
        if old_hash == new_hash:
            break
        else:
            old_hash = new_hash
            continue
    return True

def bfs_search(state, dfs_route):
    stateQueue = PriorityQueue()
    if fit_regular(state) == False: return None
    new_state = copy.deepcopy(state)
    new_state.sol_matrix = np.where(new_state.sol_matrix > 0, True, False)
    if checkSolution(new_state):
        return new_state
    stateQueue.put((len((np.where(state.isfilled_matrix==False))[0]), state))
    while not stateQueue.empty():
        notfilled_num, state = stateQueue.get()

        row_branch = None
        for row_positons in dfs_route:
            if False in state.isfilled_matrix[row_positons[1]]:
                state.isfilled_matrix[row_positons[1]] = True
                row_branch = row_positons
                break

        if row_branch == None:
            continue

        for row in row_branch[2]:

            # Cut useless branch
            continue_flag = False
            for idx, val in enumerate(state.sol_matrix[row_branch[1]]):
                if val != 0 and val != row[idx]:
                    continue_flag = True
                    break
            if continue_flag == True:
                continue

            new_state = copy.deepcopy(state)
            new_state.sol_matrix[row_branch[1]] = row

            if fit_regular(new_state) == True:
                notfilled_num = len((np.where(new_state.isfilled_matrix==False))[0])
                if settings.DEBUGG:
                    print notfilled_num, " size: ", stateQueue.qsize()
                if notfilled_num == 0:
                    new_state.sol_matrix = np.where(new_state.sol_matrix > 0, True, False)
                    if checkSolution(new_state):
                        del stateQueue
                        return new_state
                    else:
                        # print new_state.sol_matrix
                        if settings.DEBUGG:
                            print "error"
                        del new_state
                        continue
                stateQueue.put((notfilled_num, new_state))
    return None

def bfs_RL(problem):
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

    ret = bfs_search(state, dfs_route)
    return ret


if __name__ == "__main__":
    time_used = []
    p_list = readQuestionFile('./tcga2016-question.txt')

    # dfs_RL(p_list[2])

    for i in xrange(0, len(p_list)):
        cur = datetime.datetime.utcnow()
        sol = bfs_RL(p_list[i])
        print sol.sol_matrix
        time_used.append(datetime.datetime.utcnow() - cur)
        for i, t in enumerate(time_used):
            print i, t
        print "--\n\n"

