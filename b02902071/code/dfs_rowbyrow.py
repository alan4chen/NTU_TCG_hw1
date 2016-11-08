import json
import datetime
import numpy as np
from copy import copy
from tools.readQuesiontFile import readQuestionFile
from tools.structure import Solution
from tools.compositions import compositions
from tools.checker import checkSolution_indivisual, checkSolution_indivisual_col
from tools.checker import checkConstraint_indivisual, checkConstraint_indivisual_col
from tools.structure import Stack


def dfs_search(dfs_matrix, dfs_route, iterator, solution):
    if iterator == solution.n:
        # print dfs_matrix
        if checkSolution_indivisual_col(dfs_matrix, solution.n, solution.col_hint):
            return dfs_matrix
        else:
            return None
    else:
        if iterator == 0 or \
                checkConstraint_indivisual_col(dfs_matrix, solution.n,solution.col_hint):
            dfs_matrix = copy(dfs_matrix)
            for position in dfs_route[iterator]:
                # DEBUG
                # if iterator == 0:
                #     print "pos:", position
                dfs_matrix[iterator] = position
                ret = dfs_search(dfs_matrix, dfs_route, iterator+1, solution)
                if ret is not None:
                    return ret
        else:
            return None

def dfs_search_loop(dfs_matrix, dfs_route, iterator, solution):
    stack = Stack()
    stack.push((dfs_matrix, iterator))
    while not stack.isEmpty():
        dfs_matrix, iterator = stack.pop()
        if iterator == solution.n:
            if checkSolution_indivisual_col(dfs_matrix, solution.n, solution.col_hint):
                return dfs_matrix
            else:
                continue
        if iterator == 0 or \
                checkConstraint_indivisual_col(dfs_matrix, solution.n,solution.col_hint):
            for position in dfs_route[iterator]:
                dfs_matrix = copy(dfs_matrix)
                dfs_matrix[iterator] = position
                stack.push((dfs_matrix, iterator+1))
    return None



def get_row_positions(row_hint, n):
    if len(row_hint) == 0:
        return [[False] * n]
    if sum(row_hint) + len(row_hint) - 1 > n:
        return None
    positions = []
    zero_n = n - sum(row_hint) - len(row_hint) + 1
    for zero_add in compositions(zero_n, len(row_hint)+1):
        ret = []
        iter_zero_add = iter(zero_add)
        iter_hint = iter(row_hint)
        ret += [False] * next(iter_zero_add)
        ret += [True] * next(iter_hint)
        for i in xrange(0, len(row_hint)-1):
            ret += [False]
            ret += [False] * next(iter_zero_add)
            ret += [True] * next(iter_hint)
        ret += [False] * next(iter_zero_add)
        positions.append(ret)
    return positions


def dfs_rowbyrow(problem):
    '''
    :param problem:
    :return: solution

    '''
    solution = Solution()
    solution.n = problem.n
    solution.row_hint = problem.row_hint
    solution.col_hint = problem.col_hint
    dfs_matrix = np.zeros((solution.n,solution.n),dtype='bool')

    dfs_route = []
    for row in solution.row_hint:
        row_positions = get_row_positions(row, solution.n)
        if row_positions is not None:
            dfs_route.append(row_positions)
        else:
            solution = None
            return solution

    ret = dfs_search(dfs_matrix, dfs_route, 0, solution)

    if ret is not None:
        solution.sol_matrix = ret
    else:
        solution = None
    return solution


if __name__ == "__main__":
    DEBUG = False

    if DEBUG:
        # test get_row_positions
        ret = get_row_positions([1,3], 5)
        for idx, pos in enumerate(ret):
            assert pos == [True, False, True, True, True]
        ret = get_row_positions([], 5)
        for idx, pos in enumerate(ret):
            assert pos == [False, False, False, False, False]
        assert get_row_positions([1,3],4) is None
        exit()



    p_list = readQuestionFile('./tcga2016-question.txt')
    time_used = []
    for idx, p in enumerate(p_list):
        cur = datetime.datetime.utcnow()
        s = dfs_rowbyrow(p)
        flag = True
        if s is not None:
            print s.sol_matrix
        else:
            flag = False

        time_used.append((datetime.datetime.utcnow() - cur, flag))
        for i, t in enumerate(time_used):
            print i, t
        print "--\n\n"


    print "total time: ", datetime.datetime.utcnow()-cur
    print "average time: ", (datetime.datetime.utcnow()-cur)/ len(p_list)



    """
    boardgen.py 10 10 0.5 0.3 12345 with 2 cuts
    DFS row by row with coloumn constraint 0:01:50.971065 per problem in average

    boardgen.py 10 10 0.5 0.3 12345 with 4 cuts
    DFS row by row with coloumn constraint 0:00:04.120466 per problem in average
    """