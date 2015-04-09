import re
import sys
import table
import matplotlib.pyplot as plt

matrixFile = open(sys.argv[1], 'r')
termList = []
fractionNewTerms = []
matrix = table.readMatrix(matrixFile)

def calculateFractionNew(matrix, termList):
	allTerms = []
	numberOfNewTerms = 0

	for row in matrix[1:]:

		for cell in row[1:]:

			if re.search("[a-z]+", cell):
				
				terms = re.findall("[a-z]+", cell)
	
				allTerms.extend(terms)

	allTerms = list(set(allTerms))

	for term in allTerms:

		if term not in termList:
			numberOfNewTerms += 1
	
	return float(numberOfNewTerms) / float(len(allTerms))				


def addTerms(matrix, termList):
	
	for row in matrix[1:]:

		for cell in row[1:]:

			if re.search("[a-z]+", cell):

				terms = re.findall("[a-z]+", cell)

				termList.extend(terms)
	print "terms added"
	return list(set(termList))


for file in sys.argv[1:]:

	matrixFile = open(file, 'r')
	matrix = table.readMatrix(matrixFile)
	fractionNew = calculateFractionNew(matrix, termList)
	termList = addTerms(matrix, termList)
	fractionNewTerms.append(fractionNew)

plt.plot(fractionNewTerms, 'ro')
plt.xticks("A24", "A25", "A26", "A22", "A23", "A27")
plt.title("Fraction new words using six FlorML matrices")
plt.ylabel("fraction")
plt.xlabel("florML files")
plt.savefig("results/fraction_new_words.pdf")
plt.close()
