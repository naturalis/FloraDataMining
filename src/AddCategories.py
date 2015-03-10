import sys
import re
import SplitColumns
import CategorizeNominals
import ClearNumerics
import ConstructCategoryMatrix

matrixFile = open(sys.argv[1], "r")
termsAndCat = open(sys.argv[2], "r")
#termsAndClasses = open(sys.argv[2], "r")
matrix = []
#rangeRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?-[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?'
#dimensionRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))? x [0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?'
#maxRegex = '(to|up to|to over) [0-9]+(\.[0-9]+)?'
#minRegex = '(above|from) [0-9]+(\.[0-9]+)?'
#lenRegex = '[0-9]+(\.[0-9]+) (long|in diam)'
#widRegex = '[0-9]+(\.[0-9]+) (wide|thick)'
output = open("matrix_new_2.tsv", "w")


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

matrix = SplitColumns.initSplitting(termsAndCat, matrix)

#CategorizeNominals.readTermsAndClasses(termsAndRegex, matrix)

#termList = CategorizeNominals.searchNewTerms(matrix)

#CategorizeNominals.filterTerms(matrix, termList, termsAndRegex)

termsAndCat.seek(0)

matrix = ConstructCategoryMatrix.initBitCodingMultipleCat(matrix, termsAndCat)

ClearNumerics.initializeDivideNumerics(matrix)

matrix = ClearNumerics.rowNumbersNotInRange(matrix)

matrix = map(list, zip(*matrix))

printMatrixToTsv(matrix)
