import operator
from operator import itemgetter

golf_terms={
	-1 : "birdie" ,
	-2 : "eagle" ,
	-3 : "albatross" ,
	0 : "par" ,
	1 : "bogey" ,
	2 : "double bogey" ,
	3 : "triple bogey" 
}

def getscore(par,swing):
	# swing = 1 returns ace regardless of par value
	if swing == 1: 
		return ("ace", -4)

	relation = swing - par
	if relation >= 4:
		return ("you suck at golf, try fishing instead", relation)
	else:
		return (golf_terms[relation], relation)

def get_ranking(score):
	# current scores from friends
	init_ranking=[
		("Dharshana", -1, 'birdie'),
		("Mohika", 0, 'par'),
		("Chelle", 3, 'triple bogey')
	]
	# add new record to ranking
	init_ranking.append(["Sze Tyng",score[1], score[0]])

	sorted_rank = sorted(init_ranking, key = itemgetter(1))

	for i in range(len(sorted_rank)):
		print(str(i+1) + ". " + sorted_rank[i][0] + "\t" + sorted_rank[i][2])

score = getscore(5,4)
get_ranking(score)
