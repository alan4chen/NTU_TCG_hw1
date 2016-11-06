import numpy as np

def findBlackSegmentInRange(matrix, row_num, s, e):
    ret_list = []
    count = 0
    start = 0
    for idx, x in enumerate(matrix[row_num][s:e+1]):
        if x == 1 and count == 0:
            count += 1
            start = idx
        elif x == 1 and count != 0:
            count += 1
        elif x != 1 and count != 0:
            ret_list.append([s+start, s+idx-1, count])
            count = 0
        elif x != 1 and count == 0:
            continue
    if count != 0:
        ret_list.append([s + start, e, count])
    return ret_list


def findBlackCells(matrix, row_num, s, e):
    cells = np.where(matrix[row_num][s:e+1] == 1)
    return map(lambda x : x + s, cells[0])

def findEmptyCells(matrix, row_num, s, e):
    cells = np.where(matrix[row_num][s:e+1] == -1)
    return map(lambda x : x + s, cells[0])

def findEmptyCellsBoundedSegments(matrix, row_num, s, e):
    ret_list = []
    count = 0
    start = 0
    for idx, x in enumerate(matrix[row_num][s:e + 1]):
        if x != -1 and count == 0:
            count += 1
            start = idx
        elif x != -1 and count != 0:
            count += 1
        elif x == -1 and count != 0:
            ret_list.append([s + start, s + idx - 1, count])
            count = 0
        elif x == -1 and count == 0:
            continue
    if count != 0:
        ret_list.append([s + start, e, count])
    return ret_list

def updateRunMatrix(state, row_num):
    run_list = []
    for i in xrange(0, state.n):
        state.row_run_matrix[row_num][i] = []
    for run_id, run in enumerate(state.row_run[row_num]):
        for x in xrange(run[0], run[1]+1):
            state.row_run_matrix[row_num][x].append(run_id)
    return

def findCellBlackSegments(matrix, row_num, cell):
    if matrix[row_num][cell] != 1:
        return [-1, -1, 0]
    ret = [cell, cell, 1]
    left = cell - 1
    right = cell + 1
    while left >= 0:
        if matrix[row_num][left] == 1:
            ret[0] = left
            left -= 1
            continue
        else:
            break
    while right < len(matrix[0]):
        if matrix[row_num][right] == 1:
            ret[1] = right
            right += 1
            continue
        else:
            break
    ret[2] = ret[1] - ret[0] + 1
    return ret


if __name__ == "__main__":

    # test 1, 2
    m = np.zeros((10,10), dtype="int")
    m[3][1] = 1
    m[3][2] = 1
    m[3][4] = 1
    m[3][5] = 1
    m[3][6] = 1
    m[3][7] = 1
    m[3][9] = 1
    assert findBlackSegmentInRange(m, 3, 1, 8) == [[1, 2, 2], [4, 7, 4]]
    assert findBlackCells(m, 3,2,8) == [2, 4, 5, 6, 7]
    assert findCellBlackSegments(m, 3, 2) == [1, 2, 2]


    # test 3
    m = np.zeros((10,10), dtype="int")
    m[3][1] = 1
    m[3][4] = -1
    m[3][5] = -1
    m[3][6] = 1
    m[3][7] = -1
    m[3][9] = 1
    assert findEmptyCellsBoundedSegments(m, 3, 1, 9) == [[1, 3, 3], [6, 6, 1], [8, 9, 2]]
    print findEmptyCellsBoundedSegments(m, 3, 4, 5)
    print findEmptyCells(m, 3, 4, 7) == [4, 5, 7]




