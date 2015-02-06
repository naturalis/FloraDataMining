import sys
import re

matrixFile = open(sys.argv[1], "r")
termsAndClasses = open(sys.argv[2], "r")
matrix = []
output = open("matrix.tsv", "w")


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


#Reads an array with strings containing terms and a list of terms. This code categorizes all arrays to a categoryNumber 	
def catOrdinals(array, categories):
	categoryNumber = 0
	categorizedArray = [0 for i in range(len(array))]

	for string in categories:
		if len(string) > 1:
			categoryNumber += 1

			for i in range(len(array)):
				if re.search(string, array[i].split(',')[0]):
					print array[i].split(',')[0]	
					categorizedArray[i] = categoryNumber
	return categorizedArray


#This code reads a matrix, a term, and a list with categories belonging to that term. It returns a matrix with integers corresponding to a category to which the values int he matrix are assigned.
def initCategorizationOrdinals(matrix, term, categoryList):		
	for i in range(1, len(matrix)):
		classes = matrix[i][0].split("/")

		if classes[len(classes) - 1] == term:
			print classes
			matrix[i][1:] = catOrdinals(matrix[i][1:], categoryList)
	return matrix


#This code reads the file containing the terms and the different class assigned to that term. The term is put on the first row aneding wiht a :. IN the next line a row with classes is shown.
def readTermsAndClasses(termsAndCategories, matrix):
	for line in termsAndCategories:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2].lower()
		elif len(line.split(',')) > 1:
			categoryList = line[:len(line) - 1].split(",")
			#When one term and its classes are found categorization of the text in the matrix with the help of the classses can start.
			print term
			matrix = initCategorizationOrdinals(matrix, term, categoryList)


def readMatrix(matrix, matrixFile):
	for line in matrixFile:
		row = line.split("\t")
		matrix.append(row)
	return matrix


matrix = readMatrix(matrix, matrixFile)
matrix = map(list, zip(*matrix))
readTermsAndClasses(termsAndClasses, matrix)
printMatrixToTsv(map(list, zip(*matrix)))
