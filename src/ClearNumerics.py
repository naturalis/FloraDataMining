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
		
		
def divideNumerics(matrix, row, regex, left, right, term):
	numberRegex = '[0-9]+(\.[0-9]+)?'

	for text in row:
		if re.search("sea( |-)level", text):
			row[row.index(text)] = '0'.join(text.split(re.search("sea( |-)level", text).group(0)))
			text = '0'.join(text.split("sea level"))
									
		if re.search(regex, text):
			
			if matrix[matrix.index(row) + 1][0] != row[0] + left:
				matrix.insert(matrix.index(row) + 1, ['-' for i in range(len(matrix[0]))])
				matrix.insert(matrix.index(row) + 2, ['-' for i in range(len(matrix[0]))])
				matrix[matrix.index(row) + 1][0] = row[0] + left
				matrix[matrix.index(row) + 2][0] = row[0] + right
				
			if term == "l":
				temp = re.search(regex, text).group(0)
				number = re.search(numberRegex, temp).group(0)
				matrix[matrix.index(row) + 1][row.index(text)] = number
					
			elif term == "r":
				temp = re.search(regex, text).group(0)
				number = re.search(numberRegex, temp).group(0)
				matrix[matrix.index(row) + 2][row.index(text)] = number	
				
			else:
				numbers = re.search(regex, text).group(0).split(term)
				matrix[matrix.index(row) + 1][row.index(text)] = numbers[0]
				matrix[matrix.index(row) + 2][row.index(text)] = numbers[1]										


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

