import settings
PRINT_TIME = settings.PRINT_TIME


def writeAnswerFile(path, answers):
    f = open(path, "w")
    for answer in answers:
        f.write("$"+str(answer[0])+"\n")
        for line in answer[1]:
            f.write('\t'.join(map(str, line))+"\n")
        if PRINT_TIME == True:
            f.write(str(answer[2]) + "\n\n")
    f.close()