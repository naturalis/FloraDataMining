import sys
import re

matrixFile = open(sys.argv[1], "r")
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


#Returns one numerical value for a range or in a text containing a numerical value
def initCategorizationNumerics(matrix):
	for i in range(1, len(matrix)):
		for j in range(1,len(matrix[0])):
			if re.search('[0-9] ', matrix[i][j]):
				matrix[i][1:] = printNumericValueArray(matrix[i][1:])
				break


def readMatrix(matrix, matrixFile):
	for line in matrixFile:
		row = line.split("\t")
		matrix.append(row)
	return matrix


matrix = readMatrix(matrix, matrixFile)
matrix = map(list, zip(*matrix))
initCategorizationNumerics(matrix)
printMatrixToTsv(map(list, zip(*matrix)))

