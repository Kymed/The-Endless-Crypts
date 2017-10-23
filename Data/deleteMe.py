with open('saveddata/scores.txt', 'r') as file:
    highscore = [line.strip().rsplit(' ', 1) for line in file if line.strip()]

from operator import itemgetter
sorted_highscore = sorted(highscore, reverse=True, key=itemgetter(1))

with open('saveddata/scores.txt', 'w') as file:
    file.write('\n'.join(['{} {}'.format(name, score) for name, score in sorted_highscore]))
