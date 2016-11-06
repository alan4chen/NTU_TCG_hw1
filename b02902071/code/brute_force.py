import json
import numpy as np
from tools.readQuesiontFile import readQuestionFile
from tools.structure import Solution
from tools.checker import checkSolution


def brute_force(problem):
    '''
    :param problem:
    :return: solution

    Complexity = O( 2^(n^2) * n^2 )
    '''
    solution = Solution()
    solution.n = problem.n
    solution.row_hint = problem.row_hint
    solution.col_hint = problem.col_hint
    fmt = "{0:0%db}" % (solution.n * solution.n)
    for i in xrange(0, pow(2, solution.n*solution.n)):
        binary_str = list(fmt.format(i))
        # print binary_str
        bool_list = list(map(bool,list(map(int, binary_str))))
        solution.sol_matrix = np.matrix(bool_list).reshape(solution.n, solution.n)
        # print solution.sol_matrix
        if checkSolution(solution):
            return solution
    return None


if __name__ == "__main__":
    p_list = readQuestionFile('./tcga2016-question.txt')
    # print brute_force(p_list[1]).sol_matrix
    for p in p_list:
        s = brute_force(p)
        if s is not None:
            print s.sol_matrix
        print "--"
