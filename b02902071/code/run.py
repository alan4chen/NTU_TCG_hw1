import sys
from tools.readQuesiontFile import readQuestionFile
from tools.writeAnswerFile import writeAnswerFile

import datetime
import numpy as np

from brute_force import brute_force
from dfs import dfs
from dfs_rowbyrow import dfs_rowbyrow
from dfs_RL import dfs_RL
from bfs_heuristic_RL import bfs_RL

if __name__ == "__main__":
    question_path, answer_path, method, problem_id = sys.argv[1:]

    problem_id = int(problem_id)

    func = dfs_rowbyrow
    if method == "brute_force":
        func = brute_force
    elif method == "dfs":
        func = dfs
    elif method == "dfs_rowbyrow":
        func = dfs_rowbyrow
    elif method == "dfs_RL":
        func = dfs_RL
    elif method == "bfs_heuristic_RL":
        func =bfs_RL
    else:
        print "Method ERROR \n"
        exit(0)

    p_list = readQuestionFile('./tcga2016-question.txt')

    answers = []

    total_cur = datetime.datetime.utcnow()
    if problem_id == 0:
        for idx, p in enumerate(p_list):
            cur = datetime.datetime.utcnow()
            s = func(p)
            if s is not None:
                sol = np.where(s.sol_matrix == True, 1, 0)
                used_time = datetime.datetime.utcnow()-cur
                answers.append([idx+1, sol, used_time])

                print "$" + str(idx+1)
                print sol
                print used_time
                print "--\n"

            else:
                print "$" + str(idx + 1)
                print "Error. No Solution.\n"

    elif 1 <= problem_id < len(p_list):
        cur = datetime.datetime.utcnow()
        s = func(p_list[problem_id-1])
        if s is not None:
            sol = np.where(s.sol_matrix == True, 1, 0)
            used_time = datetime.datetime.utcnow() - cur
            answers.append([problem_id, sol, used_time])

            print "$" + str(problem_id)
            print sol
            print used_time
            print "--\n"


    total_used_time = datetime.datetime.utcnow()-total_cur
    print "Total Used Time:\n", total_used_time
    writeAnswerFile(answer_path, answers)

