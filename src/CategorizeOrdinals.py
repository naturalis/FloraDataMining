import sys
import re

#matrixFile = open(sys.argv[1], "r")
#termsAndClasses = open(sys.argv[2], "r")
#matrix = []
#output = open("new_matrix.tsv", "w")


#Reads an array with strings containing terms and a list of terms. This code categorizes all arrays to a categoryNumber 	
def catOrdinals(speciesStates, categorizedArray, categories):

	for i in range(len(speciesStates)):
		categoryNumber = 0

		for string in categories:

			if len(string) > 0:
				categoryNumber += 1
				print categoryNumber
				print string
				if re.match('^' + string + '$', speciesStates[i].split(',')[0]):
					categorizedArray[i] = categoryNumber
			
					break
	return categorizedArray


#This code reads a matrix, a term, and a list with categories belonging to that term. It returns a matrix with integers corresponding to a category to which the values int he matrix are assigned.
def initCategorizationOrdinals(matrix, term, categoryList):
	lastCharacterName = ""

	for character in matrix:

		if character[0] != lastCharacterName:		
			categories = character[0].split("/") 			

			if categories[len(categories) - 1] == term:
				lastCharacterName = character[0]			
				categoryArray = [0 for i in range(len(character))]			
				categoryArray[1:] = catOrdinals(character[1:], categoryArray[1:], categoryList)
				categoryArray[0] = character[0]	
				matrix.insert(matrix.index(character), categoryArray)
		

#This code reads the file containing the terms and the different class assigned to that term. The term is put on the first row ending wiht a :. IN the next line a row with classes is shown.
def readTermsAndClasses(termsAndClasses, matrix):
	for line in termsAndClasses:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2].lower()

		#When one term and its classes are found categorization of the text in the matrix with the help of the classses can start.
		elif len(line.split(',')) > 1:
			categoryList = line[:len(line) - 1].split(",")
			initCategorizationOrdinals(matrix, term, categoryList)

	
#matrix = readMatrix(matrix, matrixFile)
#matrix = map(list, zip(*matrix))
#readTermsAndClasses(termsAndClasses, matrix)
#printMatrixToTsv(map(list, zip(*matrix)))
