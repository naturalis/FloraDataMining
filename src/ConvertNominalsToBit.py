#This code converts the states of a character to a bit string of all 
#states present in the matrix: 1 means that the state is present for the
#current species and 0 means not present. This input is a data matrix in 
#tsv format without bit values and the output is a data matrix (matrix.tsv) containing 
#a new column displaying these bit strings. 

#The bit values are first written to be printed in table form, where at the
#end the cells in a row were sticked together to form a string. The reason 
#was that initially the idea was to print a matrix for every character, 
#containing all states and species.

import sys
import re
import table

matrixFile = open(sys.argv[1], 'r')
termsAndCategories = open(sys.argv[2], 'r')
matrix = []


def constructCategoryMatrix(row, term, possibilities):
	#Constructs a matrix  for a row in a matrix. Every column 
	#represents a character state and every row represents a species.
	#When a state is present for a species and a term, the	
	#the corresponding cell shows a 1, otherwise a 0.
	categoryMatrix = [['0' for j in range(len(possibilities))] for i in range(len(row))]
	categoryMatrix[0] = possibilities

	for i in range(1, len(row)):
		categories = row[i].split(',')

		for possibility in possibilities:
			for category in categories:
				if possibility == category:
					categoryMatrix[i][possibilities.index(possibility)] = '1'
	return categoryMatrix	

def listPossibilities(matrix,term):
	#Returns a list of all possibilities present in the matrix for a 
	#particular term  
	possibilities = []

	for i in range(1, len(matrix)):
		if matrix[i][0].endswith(term) and matrix[i][0] != matrix[i + 1][0]:
 			for value in matrix[i][1:]:
				possibilities.extend(value.split(','))

	possibilities = sorted(list(set(possibilities)))

	possibilities.remove('-')
	return possibilities		
			
def initBitColumns(matrix, term):
	#This function returns a new matrix containing new columns with bit
	#strings for a particular category.
	result = matrix[:]			
	possibilities = listPossibilities(matrix, term)

	for i in range(1,len(matrix)):

		if matrix[i][0].endswith(term) and matrix[i][0] != matrix[i + 1][0]: #checks whether there is already contructed a new column. This is needed 
										     #because the code uses the character names, which are displayed in the
										     #first cell of the row.
			categoryMatrix = constructCategoryMatrix(matrix[i], term, possibilities)								     
			result.insert(result.index(matrix[i]), ['-' for cell in range(len(matrix[0]))])
			
			for j in range(1, len(result[0])):
				result[result.index(matrix[i]) - 1][j] = ''.join(categoryMatrix[j])

			result[result.index(matrix[i]) - 1][0] = matrix[i][0]
	return result


def initBitCodingMultipleCat(matrix, cat):	
	#This function initilializes the code by selecting the terms in the  
	#the file containing the terms and categories. It finally returns 
	#a new matrix containing bit strings.
	for line in cat:

		if line.endswith(':\n'):
			term = line[:len(line) - 2].lower()
			result = initBitColumns(matrix, term)
	return result			


matrix = table.readMatrix(matrixFile)
	
matrix = initBitCodingMultipleCat(map(list, zip(*matrix)), termsAndCategories)
 
table.printToTsv(map(list, zip(*matrix)))

print 'Nominals converted to bit strings'
