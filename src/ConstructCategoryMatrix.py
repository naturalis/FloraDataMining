import sys
import re

#matrixFile = open(sys.argv[1], "r")
#categoryList = open(sys.argv[2], "r")
#matrix = []
#term = "colour"

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
				
	for cell in row:

		for possibility in possibilities:

			if possibility in cell:			
				categoryMatrix[row.index(cell)][possibilities.index(possibility)] = "1"	
	return categoryMatrix
	

def listPossibilities(row, term):
	possibilities = []

 	for value in row[1:]:
		possibilities.extend(value.split(','))
	
	possibilities = list(set(possibilities))
	possibilities.remove('-')
	
	return possibilities


def initBitColumns(matrix, term):

	for row in matrix[1:]:

		if row[0].split('/')[len(row[0].split('/')) - 1] == term and row[0] != matrix[matrix.index(row) + 1][0]:
			possibilities = listPossibilities(row, term)
			categoryMatrix = constructCategoryMatrix(row, term, possibilities)

			matrix.insert(matrix.index(row), ['-' for i in range(len(matrix[0]))])
				
			for cell in row:
				print categoryMatrix[row.index(cell)]
				print "".join(categoryMatrix[row.index(cell)])
				matrix[matrix.index(row) - 1][row.index(cell)] = "".join(categoryMatrix[row.index(cell)])
	return matrix


def column(matrix, i):
	return [row[i] for row in matrix]			


def readMatrix(matrix, matrixFile):
	for line in matrixFile:
		row = line.split("\t")
		matrix.append(row)
	return matrix


#matrix = readMatrix(matrix, matrixFile)

#for line in categoryList:
#	if line.split(',')[0] == 'aquamarine':	
#		possibilities = line.split(',')		

#for i in range(1, len(matrix[0])):
#	classes = matrix[0][i].split("/")
#	if classes[len(classes) - 1 ] == term:
#		print classes
#		categoryMatrix = constructCategoryMatrix(column(matrix, 0), column(matrix ,i), possibilities)		
#		fileName = "_".join(classes) + "-matrix.tsv"			
#		output = open(fileName, "w")
#		printMatrixToTsv(categoryMatrix)

	

 

