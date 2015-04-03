import re
import sys
import table

matrixFile = open(sys.argv[1], 'r')
termList = []

matrix = table.readMatrix(matrixFile)


def addTerms(matrix, termList):
	
	for row in matrix[1:]:

		for cell in row[1:]:

			if re.search("[a-z]+", cell):

				terms = re.findall("[a-z]+", cell)

				termList.extend(terms)

	return list(set(termList))



for file in sys.argv[1:]:
	print len(matrix[0])
	matrixFile = open(file, 'r')
	matrix = table.readMatrix(matrixFile)
	numberOfTerms = len(termList)
	termList = addTerms(matrix, termList)

	print len(termList) - numberOfTerms
