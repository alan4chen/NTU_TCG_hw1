from structure import Problem


def readQuestionFile(question_path):
    problem_list = []
    p = Problem()
    with open(question_path) as f:
        lines = f.readlines()

        # Eat First Line #1
        try:
            assert lines[0][0] is '$' and lines[0][1] is '1'
        except:
            print 'First Line of Question is not #1'
            exit()

        iterlines = iter(lines)
        prev = next(iterlines)
        for content in iterlines:
            # Eat Problem Num #?
            if content[0] is '$':
                p.n = len(p.hint_content)/2
                p.col_hint = p.hint_content[:p.n]
                p.row_hint = p.hint_content[p.n:]
                problem_list.append(p)
                p = Problem()
                continue

            # Eat Hint
            content = content.replace('\n', '')
            if len(content) == 0:
                p.hint_content.append([])
            else:
                splited_content = content.split('\t')
                p.hint_content.append(list(map(int, splited_content)))

        #Append Last Problem
        p.n = len(p.hint_content) / 2
        p.col_hint = p.hint_content[:p.n]
        p.row_hint = p.hint_content[p.n:]
        problem_list.append(p)

    return problem_list


if __name__ == "__main__":
    p_list = readQuestionFile('../tcga2016-question.txt')
    for p in  p_list:
        print p.n
        print p.row_hint
        assert p.n is len(p.row_hint)
        print p.col_hint
        assert p.n is len(p.col_hint)
        print '--'