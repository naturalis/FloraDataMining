#This code modifies all numerical values in a data matrix. Dimensions 
#values are divided in length and with, and ranges in minimum and maximum. 
#New columns are constructed only displaying the numerical values for a 
#character. For the unit conversion I used some modules of the python 
#library pyuom. 

import sys
import re

import table

from Length import Length

matrixFile = open(sys.argv[1], "r")
matrix = []
output = open("matrix.tsv", "w")


def normalize(row, units, correctUnit):
	#This function reads a list of texts and a list of units. It 
	#normalizes all units in that row to a given unit. It returns a 
	#row with the units normalized.
	numberRegex = '\d+\.*\d*'

	row[0] += " (" + correctUnit + ")"

	for i in range(len(row)):
		for unit in units:			
			if unit != correctUnit:
				if re.search(" " + unit + "( |$)", row[i]):
					for number in re.findall(numberRegex, row[i]):
						value = Length(float(number), unit)
						correctedNumber = value.toUnit(correctUnit)[0]

						if len(str(correctedNumber).split('.')) == 3:
							row[i] = row[i].replace(number, str(correctedNumber))
				
					row[i] = row[i].replace(unit, correctUnit)
	return row

def selectDominatingUnit(amountUnits):
	#This function reads a dictionary with units and their occurences. 
	#It returns the most common unit.
	for key, value in amountUnits.items():

		if value == max(amountUnits.values()):	
			return key

def countUnitNumbers(row, units):
	#This method counts the numbers of different unit types for a row
	#with textsand returns a dictionary woith every unit and every 
	#number in it. 
	for cell in row:

		for key in units.keys():
	
			if re.search(" " + key + "( |$)", cell):
				units[key] += 1
	return units

def normalizeUnits(matrix):	
	#This function normalizes measurement units by looking for the 
	#name of the unit in a cell and using the most sommon used unit as
	#reference.
	for row in matrix:
		amountUnits = {"mm": 0, "cm": 0, "dm": 0, "m": 0}

		countUnitNumbers(row, amountUnits)

		correctUnit = selectDominatingUnit(amountUnits)

		if amountUnits[correctUnit] > 0:
			matrix[matrix.index(row)] = normalize(row, amountUnits.keys(), correctUnit) 	

	return matrix


def rowNumbers(matrix):
	#Inserts a new row and adds numbers to these rows which were not 
	#putted in the matrix yet where they did not belong to dimensions 
	#or ranges.
	numberRegex = '[0-9]+(\.[0-9]+)?'

	for row in matrix:
		
		if matrix.index(row) == len(matrix) - 2:
			return matrix
			
		elif row[0]!=matrix[matrix.index(row)-1][0]: 
			if (matrix[matrix.index(row)+1][0].endswith('minimum') 
	 		and row[0]!='-'):
				matrix.insert(matrix.index(row)+1, ['-' for i in range(len(row))])
				matrix[matrix.index(row) + 1][0] = matrix[matrix.index(row)][0] 
					
				for i in range(len(row)):
					if (matrix[matrix.index(row) + 2][i] == '-' and 
						matrix[matrix.index(row) + 3][i] == '-'and re.search(numberRegex, row[i])):
						matrix[matrix.index(row) + 1][i] = re.search(numberRegex, row[i]).group(0)	


def fillCell(matrix, row, cellNumber, term, n):
	#This function looks for a particular cell in a matrix. In this 
	#cell a number is selected. This number is printed at the same 
	#place n rows further in the same matrix. 
	numberRegex = '[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+)?)?'
	number = re.search(numberRegex, term).group(0)
	
	if "-" in number and not row[0].endswith("dimensions*")  and not row[0].endswith("dimensions (merged)*"):
		number = number.split("-")[n-1]

	matrix[matrix.index(row) + n][cellNumber] = number
	

		
def divideNumerics(matrix, row, regex, left, right, term):
	#This function divided the values into when needed and puts them 
	#into the correct row. It also turns "sea-level" into "0" and 
	#excludes outliers.
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


def constructCharacters(matrix, row, left, right):
	#Constructs names of new characters in a row in a matrix. Two new 
	#rows were constructed with given names (left and right) pasted to
	#it
	matrix.insert(matrix.index(row) + 1, ['-' for i in range(len(matrix[0]))])
	matrix.insert(matrix.index(row) + 2, ['-' for i in range(len(matrix[0]))])

	matrix[matrix.index(row) + 1][0] = ''.join([row[0], left])
	matrix[matrix.index(row) + 2][0] = ''.join([row[0], right])					 		


def splitValues(matrix, row, regex, regexLeft, regexRight, left, right, delimiter):
	#Reads a matrix and a particular row and uses regular expressions 
	#to distinguish values that must be splitted in left and right 
	#(ranges, dimensions) and numbers that can just be printed alone.
	for i in range(len(row)):
		expression = ''.join(['(', regex, '|', regexLeft, '|', regexRight, ')'])
		
		if re.search(expression, row[i]):
			constructCharacters(matrix, row, left, right)

			break

	divideNumerics(matrix, row, regex, left, right, delimiter)
	divideNumerics(matrix, row, regexLeft, left, right, "l")
	divideNumerics(matrix, row, regexRight, left, right, "r")


def initializeDivideNumerics(matrix):
	#Here are all values in the dimensions characterized by regular 
	#expressions and the dimensions and ranges are divided in multiple
	#values.
	numberRegex = '(ca. )?[0-9]+(\.[0-9]+)?(-[0-9]+(\.[0-9]+)?)?'
	maxRegex = ' '.join(['(up to|to over|to|no more than)',numberRegex])
	minRegex = ' '.join(['(above|from)', numberRegex])
	rangeRegex = ''.join([numberRegex, '(\(-[0-9]+\))?','-',numberRegex, 
	'(\(-[0-9]+\))?'])
	dimensionRegex = ''.join(['((up to|to over|to|above|from|no more than) )?',
	numberRegex, '(\(-[0-9]+\))? x (\([0-9]+(.[0-9]+)?-\))?', 
	'((up to|to over|to|above|from) )?',numberRegex]) 
	lenRegex = ''.join([numberRegex, '(\(-[0-9]+\))? (m|c|)?m (long)'])
	widRegex = ''.join([numberRegex, '(\(-[0-9]+\))? (m|c|)?m (wide|thick|in diam)'])
	
	for row in matrix:
		if row[0].endswith("dimensions*") or row[0].endswith("dimensions (merged)*"):
			splitValues(matrix, row, dimensionRegex, lenRegex, widRegex, "/length", "/width", " x ")
			
		elif not row[0].endswith("minimum") and not row[0].endswith("maximum"):
			splitValues(matrix, row, rangeRegex, minRegex, maxRegex, "/minimum", "/maximum", "-")


matrix = table.readMatrix(matrixFile)
matrix = map(list, zip(*matrix))

matrix = normalizeUnits(matrix)
initializeDivideNumerics(matrix)
print "numerics divided"
rowNumbers(matrix)

table.printToTsv(map(list, zip(*matrix)))
print "Numeric values formatted"

