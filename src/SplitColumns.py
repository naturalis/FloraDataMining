import sys
import re

#matrixFile = open(sys.argv[1], "r")
#termsAndRegex = open(sys.argv[2], "r")
#matrix = []
#output = open("matrix.tsv", "w")


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
					print array
					print newArray
					matrix.insert(matrix.index(array) + 1, newArray)
					break	

	return matrix


#Adds new values to the matrix 
def initSplitting(termsAndRegex, matrix):		
	for line in termsAndRegex:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2]
		if len(line.split(',')) > 1:
			regexes = line[:len(line) - 2].split(',')
			print term
			splitColumns(matrix, term, regexes)#Adds the correct terms to new columns made in the matrix
	print matrix
	return matrix


#matrix = readMatrix(matrix, matrixFile)
#initSplitting(termsAndRegex, matrix)
#printMatrixToTsv(matrix)

