import re
import sys
import table
import matplotlib.pyplot as plt

matrixFile = open(sys.argv[1], 'r')
termList = []
numberOfNewTerms = []
matrix = table.readMatrix(matrixFile)


def addTerms(matrix, termList):
	
	for row in matrix[1:]:

		for cell in row[1:]:

			if re.search("[a-z]+", cell):

				terms = re.findall("[a-z]+", cell)

				termList.extend(terms)

	return list(set(termList))



for file in sys.argv[1:]:

	matrixFile = open(file, 'r')
	matrix = table.readMatrix(matrixFile)
	numberOfTerms = len(termList)
	termList = addTerms(matrix, termList)
	numberOfNewTerms.append((len(termList) - numberOfTerms) / len(matrix[0]))
	
plt.plot(numberOfNewTerms, 'ro')
plt.show()
