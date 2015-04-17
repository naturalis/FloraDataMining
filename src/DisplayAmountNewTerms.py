#This code counts all words for some given tsv files containing a matrix. 
#With this list and words that are new added the fraction of more used 
#words in a new FlorML file is calculated. The Words in the first row and 
#column are not included. The output is a plot showing a curve which shows 
#the fraction of new words when reading a new file.


import re
import sys
import table
import matplotlib.pyplot as plt

matrixFile = open(sys.argv[1], 'r')
termList = []
fractionNewTerms = []
matrix = table.readMatrix(matrixFile)


def calculateFractionNew(matrix, termList):
	#Calculates the fraction of words in a file, that were not yet 
	#filtered from another file.
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
	#This function adds a terms to a list of terms found in a new matrix.	
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
plt.title("Fraction new words using six FlorML matrices")
plt.ylabel("fraction new words")
plt.xlabel("files")
plt.savefig("results/fraction_new_words.pdf")
plt.close()
