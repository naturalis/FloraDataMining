import sys
import re
import SplitColumns
import CategorizeOrdinals
#import ClearNumerics

matrixFile = open(sys.argv[1], "r")
#termsAndRegex = open(sys.argv[2], "r")
termsAndClasses = open(sys.argv[2], "r")
matrix = []
output = open("matrix_cat.tsv", "w")


# This function prints a matrix in tsv format, when giving the matrix as argument.
def printMatrixToTsv(matrix):	
	for i in range(len(matrix)):
		line = ""		
		for j in range(len(matrix[0])):
			matrix[i][j] = str(matrix[i][j]).replace("\t", " ") 
			line = line + matrix[i][j] + "\t"
		line = line.replace("\n", "") 
		output.write(line)
		output.write("\n")


# This code converts a file containing a matrix to a double array.
def readMatrix(matrix, matrixFile):
	for line in matrixFile:
		row = line.split("\t")
		matrix.append(row)
	return matrix


matrix = readMatrix(matrix, matrixFile)

matrix = map(list, zip(*matrix))

#matrix = SplitColumns.initSplitting(termsAndRegex, matrix)

#CategorizeOrdinals.constructNewColumns(matrix)

CategorizeOrdinals.readTermsAndClasses(termsAndClasses, matrix)

matrix = map(list, zip(*matrix))

printMatrixToTsv(matrix)
