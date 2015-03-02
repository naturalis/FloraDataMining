import sys
import re
import SplitColumns
import CategorizeNominals
import ClearNumerics
import ConstructCategoryMatrix

matrixFile = open(sys.argv[1], "r")
termsAndRegex = open(sys.argv[2], "r")
#termsAndClasses = open(sys.argv[2], "r")
matrix = []
#rangeRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?-[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?'
#dimensionRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))? x [0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?'
#maxRegex = '(to|up to|to over) [0-9]+(\.[0-9]+)?'
#minRegex = '(above|from) [0-9]+(\.[0-9]+)?'
#lenRegex = '[0-9]+(\.[0-9]+) (long|in diam)'
#widRegex = '[0-9]+(\.[0-9]+) (wide|thick)'
output = open("matrix_new.tsv", "w")


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

#CategorizeNominals.constructNewColumns(matrix)

#CategorizeNominals.readTermsAndClasses(termsAndClasses, matrix)

#for row in matrix:
#
#	if row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions" or row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions (merged)":		
#		ClearNumerics.divideNumerics(matrix, row, dimensionRegex, "/length", "/width", " x ")
#		ClearNumerics.divideNumerics(matrix, row, lenRegex, "/length", "/width", "l")
#		ClearNumerics.divideNumerics(matrix, row, widRegex, "/length", "/width", "r")
#	else:
#		ClearNumerics.divideNumerics(matrix, row, rangeRegex, "/minimum", "/maximum", "-")
#		ClearNumerics.divideNumerics(matrix, row, maxRegex, "/minimum", "/maximum", "r")
#		ClearNumerics.divideNumerics(matrix, row, minRegex, "/minimum", "/maximum", "l")

#for row in matrix:
#	if row[0].split('/')[len(row[0].split('/')) - 2] == "dimensions" or row[0].split('/')[len(row[0].split('/')) - 2] == "dimensions (merged)":
#		ClearNumerics.divideNumerics(matrix, row, rangeRegex, "/minimum", "/maximum", "-")

#termList = CategorizeNominals.searchNewTerms(matrix)

#CategorizeNominals.filterTerms(matrix, termList, termsAndRegex)

ClearNumerics.initializeDivideNumerics(matrix)

matrix = ConstructCategoryMatrix.initBitCodingMultipleCat(matrix, termsAndRegex)

matrix = map(list, zip(*matrix))

printMatrixToTsv(matrix)
