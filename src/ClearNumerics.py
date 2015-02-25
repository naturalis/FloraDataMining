import sys
import re

#matrixFile = open(sys.argv[1], "r")
#matrix = []
#output = open("matrix.tsv", "w")


def rowNumbersNotInRange(matrix):
	numberRegex = '[0-9]+(\.[0-9]+)?'

	for row in matrix:

		if matrix.index(row) == len(matrix) - 1:
			return

		elif row[0] != matrix[matrix.index(row) - 1][0]:
			
			hierarchyNextRow = matrix[matrix.index(row) + 1][0].split('/')

			if hierarchyNextRow[len(hierarchyNextRow) - 1]  == 'minimum':
				matrix.insert( matrix.index(row), ['-' for i in range(len(row))] )
				matrix[matrix.index(row) - 1][0] = matrix[matrix.index(row)][0] 
			
	
			for cell in row:
					if matrix[matrix.index(row) + 1][row.index(cell)] == '-' and matrix[matrix.index(row) + 2][row.index(cell)] == '-' and re.search(numberRegex, cell):
						matrix[matrix.index(row) - 1][row.index(cell)] = re.search(numberRegex, cell).group(0)


def fillCell(matrix, temp, n):
	numberRegex = '[0-9]+(\.[0-9]+)?'
	number = re.search(numberRegex, temp).group(0)

	matrix[matrix.index(row) + n][row.index(text)] = number


def makeRangeRows(matrix, row):
	matrix.insert(matrix.index(row) + 1, ['-' for i in range(len(matrix[0]))])
	matrix.insert(matrix.index(row) + 2, ['-' for i in range(len(matrix[0]))])

	matrix[matrix.index(row) + 1][0] = row[0] + left
	matrix[matrix.index(row) + 2][0] = row[0] + right				
	 		
		
def divideNumerics(matrix, row, regex, left, right, term):
	for text in row:

		if re.search("sea( |-)level", text):
			row[row.index(text)] = '0'.join(text.split(re.search("sea( |-)level", text).group(0)))
			text = '0'.join(text.split("sea level"))
									
		if re.search(regex, text):
			
			if matrix[matrix.index(row) + 1][0] != row[0] + left:
				makeRangeRows(matrix, row)
				
			if term == "l":
				fillCell(matrix, re.search(regex, text).group(0), 1)
					
			elif term == "r":
				fillCell(matrix, re.search(regex, text).group(0), 2)
				
			else:
				numbers = re.search(regex, text).group(0).split(term)
				matrix[matrix.index(row) + 1][row.index(text)] = numbers[0]
				matrix[matrix.index(row) + 2][row.index(text)] = numbers[1]										


def splitValues(matrix, row, regex, regexLeft, regexRight, left, right, delimiter)
	divideNumerics(matrix, row, regex, left, right, delimiter)
	divideNumerics(matrix, row, regexLeft, left, right, "l")
	divideNumerics(matrix, row, regexRigth, left, right, "r")


def initializeDivideNumerics(matrix):
	rangeRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?-[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?'
	dimensionRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))? x [0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+))?'
	maxRegex = '(to|up to|to over) [0-9]+(\.[0-9]+)?'
	minRegex = '(above|from) [0-9]+(\.[0-9]+)?'
	lenRegex = '[0-9]+(\.[0-9]+) (long|in diam)'
	widRegex = '[0-9]+(\.[0-9]+) (wide|thick)'
	
	for row in matrix:

		if row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions" or row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions (merged)":
			splitValues(matrix, row, dimensionRegex, lenRegex, widRegex, "/length", "/width", " x ")		

		else:
			splitValues(matrix, row, dimensionRegex, minRegex, maxRegex, "/minimum", "/maximum", " - ")

	for row in matrix:
		if row[0].split('/')[len(row[0].split('/')) - 2] == "dimensions" or row[0].split('/')[len(row[0].split('/')) - 2] == "dimensions (merged)":
			divideNumerics(matrix, row, rangeRegex, "/minimum", "/maximum", "-")


#Reads a number and a string containing the unit. Converts the value to mm
def convertToMm(string, number):
	if ' mm ' in string:
		return number
	elif ' cm ' in string:
		return number * 10
	elif ' dm ' in string:
		return number * 100
	elif re.search(' m(" "|$)', string):
		print string
		return number * 1000
	else:
		return number


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
			print number
			print array[i]
			array[i] = convertToMm(array[i], int(number))
			print array[i]
	return array	


#Returns one numerical value for a range or in a text containing a numerical value
def initCategorizationNumerics(matrix):
	for i in range(1, len(matrix)):
		for j in range(1,len(matrix[0])):
			if re.search('[0-9] ', matrix[i][j]):
				print matrix[i][1:]
				matrix[i][1:] = printNumericValueArray(matrix[i][1:])
				break


#matrix = readMatrix(matrix, matrixFile)
#matrix = map(list, zip(*matrix))
#initCategorizationNumerics(matrix)
#printMatrixToTsv(map(list, zip(*matrix)))

