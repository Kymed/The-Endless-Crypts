# Score sorter from highest to lowest
# Credits: Ryan Haining from Stackoverflow
# What I (Kyle Meade) did: paragraph 2 and the "reverse=True" in scores.sort
# Also made it a function with path

def sortScores(path):
    
    # paragraph 1
    scores = []
    with open(path) as f:
        for line in f:
            name, score = line.split(' ')
            score = int(score)
            scores.append((name, score))

    scores.sort(key=lambda s: s[1], reverse=True)


    # paragraph 2
    sorted_file = open(path, "w")
    for name, score in scores:
        text = "%s %d" %(name, score)
        sorted_file.write(text)
        sorted_file.write("\n")
    sorted_file.close()    
