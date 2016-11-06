import json
import numpy as np
from copy import copy
from tools.readQuesiontFile import readQuestionFile
from tools.structure import Solution
from tools.checker import checkSolution_indivisual
from tools.checker import checkConstraint_indivisual


def dfs_search(dfs_matrix, dfs_route, iterator, solution):
    if iterator == solution.n * solution.n:
        # print dfs_matrix
        if checkSolution_indivisual(dfs_matrix, solution.n, solution.row_hint,
                                     solution.col_hint):
            return dfs_matrix
        else:
            return None
    else:
        if iterator == 0 or \
            checkConstraint_indivisual(dfs_matrix, solution.n, solution.row_hint,
                                     solution.col_hint):
            dfs_matrix = copy(dfs_matrix)
            dfs_matrix[dfs_route[iterator][0], dfs_route[iterator][1]] = True
            ret = dfs_search(dfs_matrix, dfs_route, iterator+1, solution)
            if ret is not None:
                return ret
            dfs_matrix[dfs_route[iterator][0], dfs_route[iterator][1]] = False
            ret = dfs_search(dfs_matrix, dfs_route, iterator+1, solution)
            if ret is not None:
                return ret
        else:
            return None

def dfs(problem):
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
    for i in xrange(0, solution.n):
        for j in xrange(0, solution.n):
            dfs_route.append((i,j))

    ret = dfs_search(dfs_matrix, dfs_route, 0, solution)

    if ret is not None:
        solution.sol_matrix = ret
    else:
        solution = None
    return solution


if __name__ == "__main__":
    p_list = readQuestionFile('./tcga2016-question.txt')
    # s = dfs(p_list[5])
    # print p_list[5].row_hint, p_list[5].col_hint
    # print s
    # print s.sol_matrix
    for idx, p in enumerate(p_list):
        s = dfs(p)
        if s is not None:
            print s.sol_matrix
        else:
            print "Warning! NO SOLUTION!!"
            print "idx: ", idx
            exit()
        print "--"
