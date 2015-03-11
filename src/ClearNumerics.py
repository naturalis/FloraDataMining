import sys
import re
import table

matrixFile = open(sys.argv[1], "r")
matrix = []
output = open("matrix.tsv", "w")


#Reads a number and a string containing the unit. Converts the value to mm
def convertToMm(string, number):
	if ' mm ' in string:
		return number

	elif ' cm ' in string:
		return number * 10

	elif ' dm ' in string:
		return number * 100

	elif re.search(' m(" "|$)', string):
		return number * 1000

	else:
		return number


def rowNumbersNotInRange(matrix):
	numberRegex = '[0-9]+(\.[0-9]+)?'

	for row in matrix:
		
		if matrix.index(row) == len(matrix) - 2:
			return matrix

		elif row[0] != matrix[matrix.index(row) - 1][0]:
			hierarchyNextRow = matrix[matrix.index(row) + 1][0].split('/')
			
			if hierarchyNextRow[len(hierarchyNextRow) - 1]  == 'minimum' and row[0] != '-':
				matrix.insert(matrix.index(row) + 1, ['-' for i in range(len(row))])
				matrix[matrix.index(row) + 1][0] = matrix[matrix.index(row)][0] 
				
				for i in range(len(row)):

					if matrix[matrix.index(row) + 2][i] == '-' and matrix[matrix.index(row) + 3][i] == '-' and re.search(numberRegex, row[i]):
						matrix[matrix.index(row) + 1][i] = re.search(numberRegex, row[i]).group(0)	


def fillCell(matrix, row, cellNumber, temp, n):
	numberRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+)?)?'
	number = re.search(numberRegex, temp).group(0)
	
	if "-" in number and row[0].split('/')[len(row[0].split('/')) - 1] != "dimensions*" and row[0].split('/')[len(row[0].split('/')) - 1] != "dimensions (merged)*":
		number = number.split("-")[n-1]

	matrix[matrix.index(row) + n][cellNumber] = number
	

def makeRangeRows(matrix, row, left, right):
	matrix.insert(matrix.index(row) + 1, ['-' for i in range(len(matrix[0]))])
	matrix.insert(matrix.index(row) + 2, ['-' for i in range(len(matrix[0]))])

	matrix[matrix.index(row) + 1][0] = row[0] + left
	matrix[matrix.index(row) + 2][0] = row[0] + right				
	 		
		
def divideNumerics(matrix, row, regex, left, right, term):

	for i in range(len(row)):

		if re.search("sea( |-)level", row[i]):
			row[i] = '0'.join(row[i].split(re.search("sea( |-)level", row[i]).group(0)))

		if re.search("\(-[0-9]+(\.[0-9]+)?\??-?\)", row[i]):
			row[i] = ''.join(row[i].split(re.search("\(-[0-9]+(\.[0-9]+)?\??-?\)", row[i]).group(0)))
									
		if re.search(regex, row[i]):
				
			if term == "l":
				fillCell(matrix, row, i, re.search(regex, row[i]).group(0), 1)
					
			elif term == "r":
				fillCell(matrix, row, i, re.search(regex, row[i]).group(0), 2)
				
			elif len(row[i].split(term)) > 1:			
				numbers = re.search(regex, row[i]).group(0).split(term)
				matrix[matrix.index(row) + 1][i] = numbers[0]
				matrix[matrix.index(row) + 2][i] = numbers[1]										


def splitValues(matrix, row, regex, regexLeft, regexRight, left, right, delimiter):
	for i in range(len(row)):
		
		if re.search('(' + regex + '|' + regexLeft + '|' + regexRight + ')', row[i]):
			makeRangeRows(matrix, row, left, right)
			break

	divideNumerics(matrix, row, regex, left, right, delimiter)
	divideNumerics(matrix, row, regexLeft, left, right, "l")
	divideNumerics(matrix, row, regexRight, left, right, "r")


def initializeDivideNumerics(matrix):
	numberRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+)?)?'
	rangeRegex = numberRegex +'(\(-[0-9]+\))?' + '-' + numberRegex + '(\(-[0-9]+\))?'
	dimensionRegex = numberRegex + '(\(-[0-9]+\))?' + ' x ' '(\([0-9]+(.[0-9]+)?-\))?' + numberRegex + '(\(-[0-9]+\))?'
	maxRegex = '(up to|to over|to) ' + numberRegex
	minRegex = '(above|from) ' + numberRegex
	lenRegex = numberRegex + '(\(-[0-9]+\))? (m|c|)?m (long)'
	widRegex = numberRegex + '(\(-[0-9]+\))? (m|c|)?m (wide|thick|in diam)'
	
	for row in matrix:

		if row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions*" or row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions (merged)*":
			splitValues(matrix, row, dimensionRegex, lenRegex, widRegex, "/length", "/width", " x ")
			
		elif row[0].split('/')[len(row[0].split('/')) - 1] != "minimum" and row[0].split('/')[len(row[0].split('/')) - 1] != "maximum":
			splitValues(matrix, row, rangeRegex, minRegex, maxRegex, "/minimum", "/maximum", "-")





#Reads a string containing a float and returns this numerical value as float.
def categorizeFloat(string):
	number =  float(re.search('[0-9]+\.[0-9]+', string).group(0))
	return convertToMm(string, number)


def splitRange(matrix, i, term):
	newColumn = [0 for i in range(len(matrix[0]))]
	matrix.insert(i + 1, newColumn)
	matrix.insert(i + 2, newColumn)
	matrix[i+1][0] = term + '/' + "minimum"
	matrix[i+2][0] = term + '/' + "maximum"	 


#Reads a range and returns the highest value in that range.
def categorizeRange(string):
	numberRange = re.search('[0-9]+-[0-9]+', string).group(0)
	return numberRange.split('-')


#This code reads a string containing a float in a range and returns the highest value in the range.
def categorizeFloatRange(string):
	match = re.search('[0-9]-[0-9]+\.[0-9]+', string).group(0)
	number = float(match[2:])
	return convertToMm(string, number)


#This code reads an array with strings containing numerical values. It returns an array with all values converted to one numeric float or int
def printNumericValueArray(matrix, array):
	for i in range(len(array)):
		if array[i] == '-':
			array[i] = 0

		elif re.search('[0-9]-[0-9]+\.[0-9]+', array[i]):
			splitRange(matrix, matrix.index(array), array[0])
			categories = categorizeFloatRange(array[i])
			matrix[matrix.index(array) + 1] = categories[0]
			matrix[matrix.index(array) + 2] = categories[2]

		elif re.search('[0-9]+-[0-9]+', array[i]):
			array[i] = categorizeRange(array[i])
		elif re.search('[0-9]+\.[0-9]+', array[i]):
			array[i] = categorizeFloat(array[i])
		elif re.search('[0-9]+', array[i]):
			number = re.search('[0-9]+', array[i]).group(0)
			array[i] = convertToMm(array[i], int(number))

	return array	


#Returns one numerical value for a range or in a text containing a numerical value
def initCategorizationNumerics(matrix):
	for i in range(1, len(matrix)):
		for j in range(1,len(matrix[0])):
			if re.search('[0-9] ', matrix[i][j]):
				matrix[i][1:] = printNumericValueArray(matrix[i][1:])
				break


matrix = table.readMatrix(matrixFile)


matrix = map(list, zip(*matrix))

initializeDivideNumerics(matrix)

table.printToTsv(map(list, zip(*matrix)))

