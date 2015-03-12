import sys
import re
import table

matrixFile = open(sys.argv[1], "r")
termsAndCategories = open(sys.argv[2], "r")
matrix = []


def constructColumns(array):

	for cell in array:

		if cell.split(',') > 1:
			
			for term in array.split(','):
				array.append(term)
				array.remove(array[array.index(term)])
	return set(array)							


def ConstructNewArray(rows):
	columns = constructColumns(rows)
	newMatrix = [[0 for j in range(len(columns) + 1)] for i in range(len(array) + 1)]

	for i in range(1, len(newMatrix) + 1):

		for j in range(1, len(newMatrix[0] + 1)):

			if matrix[0][j] in matrix[i][0]:
				matrix[i][j] = 1


# This function prints a matrix in tsv format, when giving the matrix as argument.
def printMatrixToTsv(m):
	
	for i in range(len(m)):
		line = ""
		
		for j in range(len(m[0])):
			m[i][j] = str(m[i][j]).replace("\t", " ") 
			line = line + str(m[i][j]) + "\t"

		line = line.replace("\n", "") 

		output.write(line)
		output.write("\n")
	

def constructCategoryMatrix(row, term, possibilities):
	categoryMatrix = [["0" for j in range(len(possibilities))] for i in range(len(row))]
	categoryMatrix[0] = possibilities

	for i in range(1, len(row)):
		categories = row[i].split(",")

		for possibility in possibilities:

			for category in categories:

				if possibility == category:
					categoryMatrix[i][possibilities.index(possibility)] = "1"
	return categoryMatrix
	

def listPossibilities(matrix,term):
	possibilities = []

	for i in range(1, len(matrix)):

		if matrix[i][0].split('/')[len(matrix[i][0].split('/')) - 1] == term and matrix[i][0] != matrix[i + 1][0]:

 			for value in matrix[i][1:]:
				possibilities.extend(value.split(','))

	possibilities = list(set(possibilities))

	possibilities.remove('-')

	return possibilities		
			

def initBitColumns(matrix, term):
	result = matrix[:][:]			
	possibilities = listPossibilities(matrix, term)

	for i in range(1,len(matrix)):

		if matrix[i][0].split('/')[len(matrix[i][0].split('/')) - 1] == term and matrix[i][0] != matrix[i + 1][0]:
			categoryMatrix = constructCategoryMatrix(matrix[i], term, possibilities)
			
			result.insert(result.index(matrix[i]), ['-' for cell in range(len(matrix[0]))])
			
			for j in range(1, len(result[0])):
				result[result.index(matrix[i]) - 1][j] = "".join(categoryMatrix[j])

			result[result.index(matrix[i]) - 1][0] = matrix[i][0]
	return result


def initBitCodingMultipleCat(matrix, cat):	

	for line in cat:

		if line[len(line) - 2] == ':':
			matrix = initBitColumns(matrix, line[:len(line) - 2].lower())
	return matrix


def column(matrix, i):

	return [row[i] for row in matrix]			


matrix = table.readMatrix(matrixFile)
	
matrix = initBitCodingMultipleCat(map(list, zip(*matrix)), termsAndCategories)
 
table.printToTsv(map(list, zip(*matrix)))
