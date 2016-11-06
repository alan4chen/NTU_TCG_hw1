import numpy as np
from structure import Solution, Problem

def getSeriesCountList(series):
    count = 0
    count_list = []
    for x in np.nditer(series, order='C'):
        if bool(x) is True:
            count += 1
        elif count is not 0:
            count_list.append(count)
            count = 0
    if count is not 0:
        count_list.append(count)
    return count_list

def getSeriesCountList_withBlank(series):
    blank_count = 0
    count = 0
    count_list = []
    for x in np.nditer(series, order='C'):
        if bool(x) is True:
            count += 1
            blank_count = 0
        elif count is not 0:
            count_list.append(count)
            count = 0
            blank_count += 1
        else:
            blank_count += 1
    if count is not 0:
        count_list.append(count)
    return count_list, blank_count

########## BruteForce Use

def checkHintSeries(hint, series):
    count_list = getSeriesCountList(series)
    if len(count_list) != len(hint):
        return False
    for i in xrange(0, len(count_list)):
        if count_list[i] != hint[i]:
            return False
    return True

def checkSolution(solution):
    for i in xrange(0, solution.n):
        if checkHintSeries(solution.row_hint[i], solution.sol_matrix[i, :]) is False:
            return False
        if checkHintSeries(solution.col_hint[i], solution.sol_matrix[:, i]) is False:
            return False
    return True

def checkSolution_indivisual(sol_matrix, n, row_hint, col_hint):
    for i in xrange(0, n):
        if checkHintSeries(row_hint[i], sol_matrix[i, :]) is False:
            return False
        if checkHintSeries(col_hint[i], sol_matrix[:, i]) is False:
            return False
    return True

def checkSolution_indivisual_col(sol_matrix, n, col_hint):
    for i in xrange(0, n):
        if checkHintSeries(col_hint[i], sol_matrix[:, i]) is False:
            return False
    return True

######### DFS Use


## Pruning in dfs
def checkHintSeriesConstraint(hint, series):
    count_list, blank_count = getSeriesCountList_withBlank(series)
    # print hint, series, count_list

    # Cut 1:  len(count_list) > len(hint)
    if len(count_list) > len(hint):
        return False

    # Cut 2: count_list and hint not same
    for i in xrange(0, len(count_list)):
        if i != len(count_list)-1 and count_list[i] != hint[i]:
            return False
        elif count_list[i] > hint[i]:
            return False

    # Cut 3: not enough to put more black segment
    if len(count_list) != 0 and len(count_list) + blank_count/2 < len(hint):
        return False
    elif len(count_list) + blank_count/2 + 1 < len(hint):
        return False

    # Cut 3 not enough cell to put more black segment
    sum_diff = sum(hint)-sum(count_list)
    len_diff = len(hint) - len(count_list)
    if len(count_list) != 0 and \
        sum_diff + len_diff > blank_count:
        return False
    elif sum_diff + len_diff - 1 > blank_count:
        return False

    return True

def checkConstraint_indivisual(matrix, n, row_hint, col_hint):
    for i in xrange(0, n):
        if checkHintSeriesConstraint(row_hint[i], matrix[i, :]) is False:
            return False
        if checkHintSeriesConstraint(col_hint[i], matrix[:, i]) is False:
            return False
    return True

def checkConstraint_indivisual_col(matrix, n, col_hint):
    for i in xrange(0, n):
        if checkHintSeriesConstraint(col_hint[i], matrix[:, i]) is False:
            return False
    return True


if __name__ == '__main__':


    # test getSeriesCountList_withBlank
    count_list, blank_count = getSeriesCountList_withBlank(np.matrix([[True, False]], dtype='bool'))
    assert blank_count is 1
    count_list, blank_count = getSeriesCountList_withBlank(np.matrix([[True, True]], dtype='bool'))
    assert blank_count is 0
    count_list, blank_count = getSeriesCountList_withBlank(np.matrix([[False, False]], dtype='bool'))
    assert blank_count is 2
    count_list, blank_count = getSeriesCountList_withBlank(np.matrix([[True, False, True, False, False]], dtype='bool'))
    assert blank_count is 2

    # test checkConstraint_indivisual 1
    n = 2
    row_hint = [[1], [1]]
    col_hint = [[1], [1]]
    matrix = np.matrix([[True, False], [False, True]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is True
    matrix = np.matrix([[True, False], [False, False]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is True
    matrix = np.matrix([[True, False], [True, True]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is False

    # test checkConstraint_indivisual 2
    n = 3
    row_hint = [[1], [1], [3]]
    col_hint = [[1,1], [1],[2]]
    matrix = np.matrix([[True, False, False], [False, False, True],[True,True,True]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is True
    matrix = np.matrix([[True, False, False], [False, False, False], [False, False, True]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is False
    matrix = np.matrix([[True, False, False], [False, False, False],[True,False,True]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is False
    matrix = np.matrix([[True, False, False], [True, False, True],[True,True,True]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is False
    matrix = np.matrix([[False, False, False], [False, False, False], [False, True, True]], dtype='bool')
    assert checkConstraint_indivisual(matrix, n, row_hint, col_hint) is False

    # test checkSolution 1
    sol = Solution()
    sol.n = 2
    sol.row_hint=[[1],[1]]
    sol.col_hint=[[1],[1]]
    sol.sol_matrix= np.matrix([[True, False],[False,True]], dtype = 'bool')
    assert checkSolution(sol) is True

    # test checkSolution 2
    sol = Solution()
    sol.n = 3
    sol.row_hint = [[1], [1], [3]]
    sol.col_hint = [[1,1], [1],[2]]
    sol.sol_matrix = np.matrix([[True, False, False], [False, False, True],[True,True,True]], dtype='bool')
    assert checkSolution(sol) is True
    sol.sol_matrix = np.matrix([[True, True, False], [False, False, True],[True,True,True]], dtype='bool')
    assert checkSolution(sol) is False

    # test checkSolution 3
    sol = Solution()
    sol.n = 2
    sol.row_hint = [[1], []]
    sol.col_hint = [[1], []]
    sol.sol_matrix = np.matrix([[True, False], [False, False]], dtype='bool')
    assert checkSolution(sol) is True
    sol.row_hint = [[2]]
    assert checkSolution(sol) is False
