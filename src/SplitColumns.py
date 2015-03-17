import sys
import re
import table

matrixFile = open(sys.argv[1], "r")
termsAndCategories = open(sys.argv[2], "r")
matrix = []


#Adds the correct terms to new columns made in the matrixdef addNewValue(matrix, i, regex):
def addNewValue(array, regexes):
	newArray = [0 for i in range(len(array))]	
			
	for i in range(1, len(array)):
		termList = []

		for regex in regexes:

			if re.search(regex, array[i]):			
				termList.append(re.search(regex, array[i]).group(0))

				for j in range(len(termList) - 1):

					if re.search(termList[0], termList[len(termList) - 1]):
						termList.pop(0)

					elif re.search(termList[len(termList) - 1], termList[j]):
						termList.pop(len(termList) - 1)	

		terms = ','.join(termList)

		if terms == "":
			terms = "-"

		newArray[i] = terms

	return newArray


#Looks for a regular expression in one of the columns of a matrix. When found, a new column is made with new term added to the hierarchy were it belongs
def splitColumns(matrix, term, regexes):
	lastTerm = ""
	newTerm = ""

	for array in matrix[1:]:
		if array[0] == newTerm:
			continue

		for i in range(1, len(array)):
			if array[0] == lastTerm:
				break
				
			for regex in regexes:
				
				if re.search(regex, array[i]):
					lastTerm = array[0]
					newTerm = array[0] + "/" + term.lower()	
					newArray = addNewValue(array, regexes)
					newArray[0] = newTerm

					matrix.insert(matrix.index(array) + 1, newArray)
					break	

	return matrix


def stemCases(cases):

	for case in cases:

		if case[len(case) - 1] == 'e':						
			stem = case[:len(case) - 1]		
			cases[cases.index(case)] = stem
	return cases

 
def markOriginalCategories(matrix):
	
	for row in matrix:
		markedOriginalTerm = row[0] + "*"
		row[0] = markedOriginalTerm

	return matrix
		

#Adds new values to the matrix 
def initSplitting(termsAndCategories, matrix):
		
	markOriginalCategories(matrix)

	for line in termsAndCategories:

		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2]

		if len(line.split(',')) > 1:
			regexes = line[:len(line) - 1].split(',')
			#regexes = stemCases(regexes)

			splitColumns(matrix, term, regexes) #Adds the correct terms to new columns made in the matrix
	return matrix


def deleteRowsAlmostEmpty(matrix):
	result = matrix[:]
	
	for row in matrix:

		if len(list(set(row))) < 10:			
			result.remove(row)
	return result


matrix = table.readMatrix(matrixFile)

matrix = map(list, zip(*matrix))			

matrix = deleteRowsAlmostEmpty(matrix)

matrix = initSplitting(termsAndCategories, matrix)

table.printToTsv(map(list, zip(*matrix)))

