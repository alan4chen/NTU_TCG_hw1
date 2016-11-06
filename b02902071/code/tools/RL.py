from structure import tranposeSolutionState
from RL_tools import *
import numpy as np
from time import sleep

#   Note
# class SolutionState:
#     sol_matrix = None
#     isfilled_matrix = None
#     row_run_matrix = None   [row_id]  --> row_run_matrix[row_num][column_num]
#     col_run_matrix = None
#     n = 0
#     row_hint = None    row_len --> row_hint[row_num][row_id]
#     col_hint = None
#     row_run = None    (s, e) --> row_run[row_num][row_id]
#     col_run = None
#     transpose = False


def rule_1_1(state):
    for row_num, rowRun in enumerate(state.row_run):
        for idx, run in enumerate(rowRun):
            LB = state.row_hint[row_num][idx]
            u = run[1]-run[0]+1-LB
            for cell_i in range(run[0] + u, run[1] - u + 1):
                if state.isfilled_matrix[row_num][cell_i]:
                    continue
                if state.sol_matrix[row_num][cell_i]  == -1 : return False
                state.sol_matrix[row_num][cell_i] = 1
                state.isfilled_matrix[row_num][cell_i] = True
    return True

def rule_1_2(state):
    empty_cells_tmp = np.where(state.isfilled_matrix == False)
    empty_cells = zip(empty_cells_tmp[0], empty_cells_tmp[1])
    for cell in empty_cells:
        if len(state.row_run[cell[0]]) == 0:
            for i in xrange(0, state.n):
                if state.sol_matrix[cell[0]][i] == 1: return False
                state.sol_matrix[cell[0]][i] = -1
                state.isfilled_matrix[cell[0]][i] = True
            continue
        if 0 <= cell[1] < state.row_run[cell[0]][0][0] or \
                state.row_run[cell[0]][-1][1] < cell[1] < state.n:
            if state.sol_matrix[cell[0]][cell[1]] == 1: return False
            state.sol_matrix[cell[0]][cell[1]] = -1
            state.isfilled_matrix[cell[0]][cell[1]] = True
            continue
        for j in xrange(0, len(state.row_run[cell[0]])-1):
            if state.row_run[cell[0]][j][1] < cell[1] < state.row_run[cell[0]][j+1][0]:
                if state.sol_matrix[cell[0]][cell[1]] == 1: return False
                state.sol_matrix[cell[0]][cell[1]] = -1
                state.isfilled_matrix[cell[0]][cell[1]] = True
    return True

def rule_1_3(state):
    for row_num, rowRuns in enumerate(state.row_run):
        for idx, run in enumerate(rowRuns): # run = [s, e]
            # 1_3_1
            if run[0] > 0 and state.sol_matrix[row_num][run[0]] == 1:
                         #  and len(state.row_run_matrix[row_num][run[0]]) > 1:
                flag = True
                for run_id in state.row_run_matrix[row_num][run[0]]:
                    if run_id == idx:
                        continue
                    if state.row_hint[row_num][run_id] != 1:
                        flag = False
                if flag == True:
                    if state.sol_matrix[row_num][run[0] - 1] == 1: raise()
                    state.sol_matrix[row_num][run[0]-1] = -1
                    state.isfilled_matrix[row_num][run[0]-1] = True

            # 1_3_2
            if run[1] < state.n-1 and state.sol_matrix[row_num][run[1]] == 1:
                          # and  len(state.row_run_matrix[row_num][run[1]]) > 1:
                flag = True
                for run_id in state.row_run_matrix[row_num][run[1]]:
                    if run_id == idx:
                        continue
                    if state.row_hint[row_num][run_id] != 1:
                        flag = False
                if flag == True:
                    # print state.sol_matrix
                    # print row_num, run[1], run[1]+1
                    # print row_num, idx, run
                    if state.sol_matrix[row_num][run[1] + 1] == 1: raise()
                    state.sol_matrix[row_num][run[1]+1] = -1
                    state.isfilled_matrix[row_num][run[1]+1] = True
    return True

def rule_1_4(state):
    empty_cells_tmp = np.where(state.isfilled_matrix == False)
    empty_cells = zip(empty_cells_tmp[0], empty_cells_tmp[1])
    for cell in empty_cells:
        if 0 < cell[1] < state.n-1 and state.sol_matrix[cell[0]][cell[1]-1] == 1 and \
                state.sol_matrix[cell[0]][cell[1]+1] == 1:
            run_ids = list(set(state.row_run_matrix[cell[0]][cell[1]-1]) & set(state.row_run_matrix[cell[0]][cell[1]]) &
                 set(state.row_run_matrix[cell[0]][cell[1]+1]))
            if len(run_ids) == 0:
                continue
            run_lens = map(lambda x: state.row_hint[cell[0]][x], run_ids)
            max_len = max(run_lens)
            black_count = 1
            left_i = cell[1]-1
            right_i = cell[1]+1
            while left_i > 0:
                if state.sol_matrix[cell[0]][left_i] != 1:
                    break
                black_count += 1
                left_i -= 1
            while right_i < state.n:
                if state.sol_matrix[cell[0]][right_i] != 1:
                    break
                black_count += 1
                right_i += 1
            if max_len < black_count:
                if state.sol_matrix[cell[0]][cell[1]] == 1: return False
                state.sol_matrix[cell[0]][cell[1]] = -1
                state.isfilled_matrix[cell[0]][cell[1]] = True
    return True


def rule_1_5(state):
    black_cells_tmp = np.where(state.sol_matrix == 1)
    black_cells = zip(black_cells_tmp[0], black_cells_tmp[1])
    for cell in black_cells:
        if cell[1] > 0 and state.sol_matrix[cell[0]][cell[1]-1] < 1:
            run_ids = state.row_run_matrix[cell[0]][cell[1]]
            # print run_ids, cell[0], cell[1]
            # print state.sol_matrix
            # print state.row_run[cell[0]]
            # if cell[0] == 7 and cell[1] == 7:
            #     print state.sol_matrix
            #     print "cell77: ", state.row_run[7]
            minL = min(map(lambda x: state.row_hint[cell[0]][x], run_ids))
            m = None
            m_find = cell[1] - 1
            while m_find >= cell[1] - minL + 1:
                if m_find == -1:
                    m = -1
                    break
                if state.sol_matrix[cell[0]][m_find] == -1:
                    m = m_find
                    break
                m_find -= 1
            if m != None:
                # print state.sol_matrix
                # print cell, m, minL, state.sol_matrix[cell[0]][m]
                for j in xrange(cell[1]+1, m + minL + 1):
                    if state.sol_matrix[cell[0]][j] == -1: return False
                    state.sol_matrix[cell[0]][j] = 1
                    state.isfilled_matrix[cell[0]][j] = True
            cell_contained_lens = map(lambda x: state.row_hint[cell[0]][x], state.row_run_matrix[cell[0]][cell[1]])
            if len(set(cell_contained_lens)) == 1:
                cell_black_segment = findCellBlackSegments(state.sol_matrix,cell[0], cell[1])
                if cell_contained_lens[0] == cell_black_segment[2]:
                    if cell_black_segment[0] != 0:
                        if state.sol_matrix[cell[0]][cell_black_segment[0] - 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[0]-1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[0]-1] = True
                    if cell_black_segment[1] != state.n-1:
                        if state.sol_matrix[cell[0]][cell_black_segment[1] + 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[1] + 1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[1] + 1] = True
        elif cell[1] == 0:
            # print state.sol_matrix
            # print state.row_run_matrix
            # print cell[0], cell[1]
            run_ids = state.row_run_matrix[cell[0]][cell[1]]
            minL = min(map(lambda x: state.row_hint[cell[0]][x], run_ids))
            m = -1
            for j in xrange(cell[1] + 1, m + minL + 1):
                if state.sol_matrix[cell[0]][j] == -1: return False
                state.sol_matrix[cell[0]][j] = 1
                state.isfilled_matrix[cell[0]][j] = True
            cell_contained_lens = map(lambda x: state.row_hint[cell[0]][x], state.row_run_matrix[cell[0]][cell[1]])
            if len(set(cell_contained_lens)) == 1:
                cell_black_segment = findCellBlackSegments(state.sol_matrix, cell[0], cell[1])
                if cell_contained_lens[0] == cell_black_segment[2]:
                    if cell_black_segment[0] != 0:
                        if state.sol_matrix[cell[0]][cell_black_segment[0] - 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[0] - 1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[0] - 1] = True
                    if cell_black_segment[1] != state.n - 1:
                        if state.sol_matrix[cell[0]][cell_black_segment[1] + 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[1] + 1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[1] + 1] = True
        if cell[1] < state.n-1 and state.sol_matrix[cell[0]][cell[1]+1] < 1:
            run_ids = state.row_run_matrix[cell[0]][cell[1]]
            minL = min(map(lambda x: state.row_hint[cell[0]][x], run_ids))
            m = None
            m_find = cell[1] + 1
            while m_find <= cell[1] + minL - 1:
                if m_find == state.n:
                    m = state.n
                    break
                if state.sol_matrix[cell[0]][m_find] == -1:
                    m = m_find
                    break
                m_find += 1
            if m != None:
                for j in xrange(m - minL , cell[1]):
                    if state.sol_matrix[cell[0]][j] == -1: return False
                    state.sol_matrix[cell[0]][j] = 1
                    state.isfilled_matrix[cell[0]][j] = True
            cell_contained_lens = map(lambda x: state.row_hint[cell[0]][x], state.row_run_matrix[cell[0]][cell[1]])
            if len(set(cell_contained_lens)) == 1:
                cell_black_segment = findCellBlackSegments(state.sol_matrix, cell[0], cell[1])
                if cell_contained_lens[0] == cell_black_segment[2]:
                    if cell_black_segment[0] != 0:
                        if state.sol_matrix[cell[0]][cell_black_segment[0] - 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[0] - 1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[0] - 1] = True
                    if cell_black_segment[1] != state.n - 1:
                        if state.sol_matrix[cell[0]][cell_black_segment[1] + 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[1] + 1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[1] + 1] = True
        elif cell[1] == state.n - 1:
            runs = state.row_run_matrix[cell[0]][cell[1]]
            minL = min(map(lambda x: state.row_hint[cell[0]][x], runs))
            m = state.n
            for j in xrange(m - minL, cell[1]):
                if state.sol_matrix[cell[0]][j] == -1: return False
                state.sol_matrix[cell[0]][j] = 1
                state.isfilled_matrix[cell[0]][j] = True
            cell_contained_lens = map(lambda x: state.row_hint[cell[0]][x], state.row_run_matrix[cell[0]][cell[1]])
            if len(set(cell_contained_lens)) == 1:
                cell_black_segment = findCellBlackSegments(state.sol_matrix, cell[0], cell[1])
                if cell_contained_lens[0] == cell_black_segment[2]:
                    if cell_black_segment[0] != 0:
                        if state.sol_matrix[cell[0]][cell_black_segment[0] - 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[0] - 1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[0] - 1] = True
                    if cell_black_segment[1] != state.n - 1:
                        if state.sol_matrix[cell[0]][cell_black_segment[1] + 1] == 1: return False
                        state.sol_matrix[cell[0]][cell_black_segment[1] + 1] = -1
                        state.isfilled_matrix[cell[0]][cell_black_segment[1] + 1] = True
    return True


def rule_2_1(state):
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])): # run = [s, e]
            if run_id != 0 and state.row_run[row_num][run_id][0] <= state.row_run[row_num][run_id-1][0]:
                state.row_run[row_num][run_id][0] = state.row_run[row_num][run_id-1][0] + \
                    state.row_hint[row_num][run_id-1] + 1
            if run_id != len(state.row_run[row_num]) - 1 and \
                    state.row_run[row_num][run_id][1] >= state.row_run[row_num][run_id+1][1]:
                state.row_run[row_num][run_id][1] = state.row_run[row_num][run_id+1][1] - \
                    state.row_hint[row_num][run_id+1] - 1
        updateRunMatrix(state, row_num)
    return True

def rule_2_2(state):
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])): # run = [s, e]
            if state.row_run[row_num][run_id][0] != 0 and state.sol_matrix[row_num][state.row_run[row_num][run_id][0]-1] == 1:
                state.row_run[row_num][run_id][0] += 1
            if state.row_run[row_num][run_id][1] != state.n-1 and state.sol_matrix[row_num][state.row_run[row_num][run_id][1]+1] == 1:
                state.row_run[row_num][run_id][1] -= 1
        updateRunMatrix(state, row_num)
    return True


def rule_2_3(state):
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])): # run = [s, e]
            # if row_num == 0 and run_id == 0:
            #     print state.sol_matrix
            #     print state.row_run
            run = state.row_run[row_num][run_id]
            segment_cells = findBlackSegmentInRange(state.sol_matrix, row_num, run[0], run[1])
            # if row_num == 0 and run_id == 0:
            #     print "segment_cells:", segment_cells
            #     print state.row_hint[row_num][:run_id]
            #     print state.row_hint[row_num][run_id:]
            for cell in segment_cells:
                if cell[2] <= max([0] + state.row_hint[row_num][:run_id]) and cell[2] > max([0]+state.row_hint[row_num][run_id:]):
                    state.row_run[row_num][run_id][0] = cell[1] + 2
                if cell[2] <= max([0] + state.row_hint[row_num][run_id+1:]) and cell[2] > max([0]+state.row_hint[row_num][:run_id+1]):
                    state.row_run[row_num][run_id][1] = cell[0] - 2
            # if row_num == 0 and run_id == 0:
                # print "bug:\n", state.sol_matrix
                # print "bug:\n", state.row_run
        updateRunMatrix(state, row_num)
    return True

def rule_2_4(state):
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])): # run = [s, e]
            run = state.row_run[row_num][run_id]
            left = run[0]
            while left <= run[1]:
                if state.sol_matrix[row_num][left] == -1:
                    state.row_run[row_num][run_id][0] = left + 1
                    left += 1
                else:
                    break
            right = run[1]
            while right >= run[0]:
                if state.sol_matrix[row_num][right] == -1:
                    state.row_run[row_num][run_id][1] = right - 1
                    right -= 1
                else:
                    break
        updateRunMatrix(state, row_num)
    return True


def rule_3_1(state):
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])): # run = [s, e]
            prev_end = -1
            if run_id != 0:
                prev_end = state.row_run[row_num][run_id-1][1]
            next_start = state.n
            if run_id != len(state.row_run[row_num])-1:
                next_start = state.row_run[row_num][run_id+1][0]
            black_cells = findBlackCells(state.sol_matrix, row_num, prev_end+1, next_start-1)
            black_segments = findBlackSegmentInRange(state.sol_matrix, row_num, prev_end+1, next_start-1)
            if len(black_cells) > 1 and len(black_segments) != 1:
                m = black_segments[0][0]
                n = black_segments[-1][1]+1
                for x in range(m, n):
                    if state.sol_matrix[row_num][x] == -1: return False
                    state.sol_matrix[row_num][x] = 1
                    state.isfilled_matrix[row_num][x] = True
                u = state.row_hint[row_num][run_id] - (n - m + 1)
                state.row_run[row_num][run_id][0] = m - u
                state.row_run[row_num][run_id][1] = n + u
        updateRunMatrix(state, row_num)
    return True

def rule_3_2(state):
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])): # run = [s, e]
            run = state.row_run[row_num][run_id]
            run_len = state.row_hint[row_num][run_id]
            boundedSegments = findEmptyCellsBoundedSegments(state.sol_matrix, row_num, run[0], run[1])
            # if row_num == 2 and run_id == 0:
            #     print boundedSegments, run_len
            if len(boundedSegments) > 1:
                for i in xrange(0, len(boundedSegments)):
                    if boundedSegments[i][2] < run_len:
                        continue
                    else:
                        state.row_run[row_num][run_id][0] = boundedSegments[i][0]
                        break
                for i in xrange(len(boundedSegments)-1, 0):
                    if boundedSegments[i][2] < run_len:
                        continue
                    else:
                        state.row_run[row_num][run_id][1] = boundedSegments[i][1]
                        break
                for segment in findEmptyCellsBoundedSegments(state.sol_matrix, row_num, run[0], run[1]):
                    if segment[2] < run_len and len(state.row_run_matrix[row_num][segment[0]]) == 1 and \
                            state.row_run_matrix[row_num][segment[0]][0] == run_id:
                        for i in xrange(segment[0], segment[1]+1):
                            if state.sol_matrix[row_num][i] == 1: return False
                            state.sol_matrix[row_num][i] = -1
                            state.isfilled_matrix[row_num][i] = True
        updateRunMatrix(state, row_num)
    return True

def rule_3_3(state):

    # rule 3.3.1
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])): # run = [s, e]
            run = state.row_run[row_num][run_id]
            run_len = state.row_hint[row_num][run_id]
            if state.sol_matrix[row_num][run[0]] == 1 and len(state.row_run_matrix[row_num][run[0]]) == 1 \
                    and state.row_run_matrix[row_num][run[0]][0] == run_id:
                for i in xrange(run[0]+1, run[1] + run_len - 1):
                    if state.sol_matrix[row_num][run[0]] == -1: return False
                    state.sol_matrix[row_num][run[0]] = 1
                    state.isfilled_matrix[row_num][run[0]] = True
                if run[0] != 0:
                    if state.sol_matrix[row_num][run[0] - 1] == 1: return False
                    state.sol_matrix[row_num][run[0]-1] = -1
                    state.isfilled_matrix[row_num][run[0]] = True
                if run[0]+run_len-1 != state.n-1:
                    if state.sol_matrix[row_num][run[0] + run_len] == 1: return False
                    state.sol_matrix[row_num][run[0]+run_len] = -1
                    state.isfilled_matrix[row_num][run[0]+run_len] = True
                state.row_run[row_num][run_id][1] = run[0]+run_len-1
                if len(state.row_run_matrix[row_num][run[1]]) != 1:
                    state.row_run[row_num][run_id+1][0] = run[1] + 2
                if run_id != 0 and state.row_run[row_num][run_id-1][1] == run[0] - 1:
                    state.row_run[row_num][run_id - 1][1] = run[0] - 2
        updateRunMatrix(state, row_num)
    # rule 3.3.2
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])):  # run = [s, e]
            run = state.row_run[row_num][run_id]
            if run_id == 0 or state.row_run[row_num][run_id-1][1] < run[0]:
                blackCells = findBlackCells(state.sol_matrix, row_num, run[0], run[1])
                boundedSegment = findEmptyCellsBoundedSegments(state.sol_matrix, row_num, run[0], run[1])
                if len(blackCells) != 0 and len(boundedSegment) != 0 and \
                        blackCells[0] <= boundedSegment[0][1]:
                    state.row_run[row_num][run_id][1] = boundedSegment[0][1]
        updateRunMatrix(state, row_num)

    # rule 3.3.3
    for row_num in xrange(0, len(state.row_run)):
        for run_id in xrange(0, len(state.row_run[row_num])):  # run = [s, e]
            run = state.row_run[row_num][run_id]
            run_len = state.row_hint[row_num][run_id]
            if run_id == 0 or state.row_run[row_num][run_id - 1][1] < run[0]:
                blackSegments = findBlackSegmentInRange(state.sol_matrix, row_num, run[0], run[1])
                if len(blackSegments) > 1:
                    s = blackSegments[0][0]
                    for i in xrange(1, len(blackSegments)):
                        if blackSegments[i][1] - s + 1 > run_len:
                            state.row_run[row_num][run_id][1] = blackSegments[i][1] - 2
                            break
        updateRunMatrix(state, row_num)

    return True





