import settings
PRINT_TIME = settings.PRINT_TIME


def writeAnswerFile(path, answers, total_used_time=None):
    f = open(path, "w")
    for answer in answers:
        f.write("$"+str(answer[0])+"\n")
        for line in answer[1]:
            f.write('\t'.join(map(str, line))+"\n")
        if PRINT_TIME == True:
            f.write(str(answer[2]) + "\n\n")
    if PRINT_TIME and total_used_time != None:
        f.write("Total Used Time: " +str(total_used_time) + "\n\n")
    f.close()