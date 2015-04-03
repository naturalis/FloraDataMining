import sys
import re
import table
from Length import Length

matrixFile = open(sys.argv[1], "r")
matrix = []
output = open("matrix.tsv", "w")


def normalize(row, units, correctUnit):
	numberRegex = '\d+\.*\d*'

	for i in range(len(row)):

		for unit in units:
	
			if re.search(" " + unit + "( |$)", row[i]):

				for number in re.findall(numberRegex, row[i]):
					value = Length(float(number), unit)
					correctedNumber = value.toUnit(correctUnit)[0]
					row[i] = row[i].replace(number, str(correctedNumber))
				
				row[i] = row[i].replace(unit, correctUnit)

	return row


def selectDominatingUnit(amountUnits):

	for key, value in amountUnits.items():

		if value == max(amountUnits.values()):	
			return key


def countUnitNumbers(row, units):

	for cell in row:

		for key in units.keys():
	
			if re.search(" " + key + "( |$)", cell):
				units[key] += 1
	return units


def normalizeUnits(matrix):	
	
	for row in matrix:
		amountUnits = {"mm": 0, "cm": 0, "dm": 0, "m": 0}

		countUnitNumbers(row, amountUnits)
		correctUnit = selectDominatingUnit(amountUnits)
		matrix[matrix.index(row)] = normalize(row, amountUnits.keys(), correctUnit) 	

	return matrix


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
	numberRegex = '(ca. )?[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+)?)?'
	maxRegex = '(up to|to over|to|no more than) ' + numberRegex
	minRegex = '(above|from) ' + numberRegex
	rangeRegex = numberRegex +'(\(-[0-9]+\))?' + '-' + numberRegex + '(\(-[0-9]+\))?'
	dimensionRegex = '((up to|to over|to|above|from|no more than) )?' + numberRegex + '(\(-[0-9]+\))? x (\([0-9]+(.[0-9]+)?-\))?' + '((up to|to over|to|above|from) )?' + numberRegex 
	lenRegex = numberRegex + '(\(-[0-9]+\))? (m|c|)?m (long)'
	widRegex = numberRegex + '(\(-[0-9]+\))? (m|c|)?m (wide|thick|in diam)'
	
	for row in matrix:

		if row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions*" or row[0].split('/')[len(row[0].split('/')) - 1] == "dimensions (merged)*":
			splitValues(matrix, row, dimensionRegex, lenRegex, widRegex, "/length", "/width", " x ")
			
		elif row[0].split('/')[len(row[0].split('/')) - 1] != "minimum" and row[0].split('/')[len(row[0].split('/')) - 1] != "maximum":
			splitValues(matrix, row, rangeRegex, minRegex, maxRegex, "/minimum", "/maximum", "-")


matrix = table.readMatrix(matrixFile)
matrix = map(list, zip(*matrix))

matrix = normalizeUnits(matrix)
initializeDivideNumerics(matrix)
rowNumbersNotInRange(matrix)

table.printToTsv(map(list, zip(*matrix)))
print "Numeric values formatted"

