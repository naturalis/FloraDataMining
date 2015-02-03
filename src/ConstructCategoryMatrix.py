import re

def constructCategoryMatrix(matrix, category, categoryList, possibilities)

	categoryMatrix = [[0 for i in range(len(possibilities + 1))] for i in range(len(matrix))]
	categoryMatrix[0][1:len(matrix[0]] = categoryList.split(',')
	categoryMatrix[0] = matrix[0]

	for i in range(len(matrix)):
		for j in range(1,len(possibilities) + 1):
			if re.match((possibility + ",")|(possibility + '$'), categoryList[j]):
				categoryMatrix[i][j] = 1
				break
	print categoryMatrix
			
	


	

 

