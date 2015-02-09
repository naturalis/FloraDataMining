import sys
import re

matrixFile = open(sys.argv[1], "r")
termsAndRegex = open(sys.argv[2], "r")
termsAndClasses = open(sys.argv[3], "r")
matrix = []
output = open("matrix.tsv", "w")

def fillEmptyFieldsWithFamily(rowNumber, matrix):

	for i in range(rowNumber + 1, len(matrix)):
		for j in range(1, len(matrix)):
			if matrix[i][j] == "-" or 0:
				matrix[i][j] = matrix[rowNumber[j]]
	

def fillEmptyFiledsWithGenerus(generus, rowNumber, matrix):
	for i in range(rowNumber + 1, len(matrix)):
		if genera.lower() in matrix[i][0].lower():
			for j in range(1, len(matrix[0])):
				if matrix[i][j] == "-" or matrix[i][j] == 0:
					matrix[i][j] = matrix[rowNumber][j] 


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


#Adds teh correct terms to new columns made in the matrix
def addNewValue(matrix, i, regex):
	for j in range(1, len(matrix)):
		if re.search(regex, matrix[j][i - 1]):			
			termList = re.findall(regex, matrix[j][i - 1])
			terms = ','.join(termList)
			matrix[j].insert(i, terms)
		else:
			matrix[j].insert(i, "-")


#Looks for a regular expession in one of the columns of a matrix. When found, a new column is made with new term added to rthe hierarchy were it belongs.
def splitColumns(matrix, term, regex):
	lastTerm = ""

	for j in range(1, len(matrix[0])):
		for i in range(1, len(matrix)):					
			if re.search(regex, matrix[i][j]):
				if matrix[i][j] == lastTerm:
					break	
				else:
					matrix[0].insert(j + 1, matrix[0][j] + "/" + term.lower())
					addNewValue(matrix, j + 1, regex)
					lastTerm = matrix[i][j + 1]
					break


#Adds new values to the matrix 
def initSplitting(termsAndRegex, matrix):		
	for line in termsAndRegex:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2]
		if line[0] == "(":
			regex = line[:len(line) - 1]
			splitColumns(matrix, term, regex)


#Counts the different number of classes in each row in a matrix
def countClasses(matrix):
	for j in range(1, len(matrix[0])):
		tempRow = []
		count = 0
		for i in range(1, len(matrix)):
			tempRow.append(matrix[i][j])	
		for string in tempRow:
			if string != "-":
				count += 1		
		set = {}
  		map(set.__setitem__, tempRow, [])
		print matrix[0][j]
		print len(set.keys()) 
	

#Reads an array with strings containing terms and a list of terms. It returns a list of lists with bit codes: 1 means the term is present in the string, and 0 means the term is not present.
	bitList = [0 for i in range(len(terms))]							
	i = 0

	for category in terms:
		if category in string:
			bitList[i] = 1
		i += 1	


#Reads an array with strings containing terms and a list of terms. This code categorizes all arrays to a categoryNumber 	
def categorizeOrdinals(array, categories):
	categoryNumber = 0
	categorizedArray = [0 for i in range(len(array))]

	for string in categories:
		categoryNumber += 1
		print string
		for i in range(len(array)):
			if re.search(string, array[i].split(',')[0]):
				categorizedArray[i] = categoryNumber
	return categorizedArray


#Reads a number and a string containing the unit. Converts the value to mm
def convertToMm(string, number):
	if ' mm ' in string:
		return number
	elif ' cm ' in string:
		return number * 10
	elif ' dm ' in string:
		return number * 100
	elif re.search(' m([^a-z])', string):
		return number * 1000
	else:
		return number


#Reads a string containing a float and returns this numerical value as float.
def categorizeFloat(string):
	number =  float(re.search('[0-9]+\.[0-9]+', string).group(0))
	
	return convertToMm(string, number)


#Reads a range and returns the highest value in that range.
def categorizeRange(string):
	numberRange = re.search('[0-9]+-[0-9]+', string).group(0)
	numbers = numberRange.split('-')
	lowest = numbers[0]
	highest = numbers[1]
	return convertToMm(string, int(highest))	


#This code reads a string containing a float in a range and returns the highest value in the range.
def categorizeFloatRange(string):
	match = re.search('[0-9]-[0-9]+\.[0-9]+', string).group(0)
	number = float(match[2:])
	return convertToMm(string, number)


#This code reads an array with strings containing numerical values. It returns an array with all values converted to one numeric float or int
def printNumericValueArray(array):
	for i in range(len(array)):
		if array[i] == '-':
			array[i] = 0
		elif re.search('[0-9]-[0-9]+\.[0-9]+', array[i]):
			array[i] = categorizeFloatRange(array[i])
		elif re.search('[0-9]+-[0-9]+', array[i]):
			array[i] = categorizeRange(array[i])
		elif re.search('[0-9]+\.[0-9]+', array[i]):
			array[i] = categorizeFloat(array[i])
		elif re.search('[0-9]+', array[i]):
			number = re.search('[0-9]+', array[i]).group(0)
			array[i] = convertToMm(array[i], int(number))
	return array


#This code reads a matrix, a term, and a list with categories belonging to that term. It returns a matrix with integers corresponding to a category to which the values int he matrix are assigned.
def initCategorizationOrdinals(matrix, term, categoryList):		
	for i in range(1, len(matrix)):
		classes = matrix[i][0].split("/")

		if classes[len(classes) -1 ] == term:
			matrix[i][1:] = categorizeOrdinals(matrix[i][1:], categoryList)
	return matrix

	
#This code reads the file containing the terms and the different class assigned to that term. The term is put on the first row aneding with a :. IN the next line a row with classes is shown.
def readTermsAndClasses(termsAndCategories, matrix):
	for line in termsAndCategories:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2].lower()
		elif line.split(',') > 0:	
			categoryList = line[:len(line) - 1].split(",")
			#When one term and its classes are found categorization of the text in the matrix with the help of the classses can start.
			matrix = initCategorizationOrdinals(matrix, term, categoryList)


#Returns one numerical value for a range or in a text containing a numerical value
def initCategorizationNumerics(matrix):
	for i in range(1, len(matrix)):
		if all(isinstance(item, str) for item in matrix[i]):
			matrix[i][1:] = printNumericValueArray(matrix[i][1:])		
	

def readMatrix(matrix, matrixFile):
	for line in matrixFile:
		row = line.split("\t")
		matrix.append(row)
	return matrix


matrix = readMatrix(matrix, matrixFile)
matrix = map(list, zip(*matrix))

readTermsAndClasses(termsAndClasses, matrix)
initCategorizationNumerics(matrix)

printMatrixToTsv(map(list, zip(*matrix)))
