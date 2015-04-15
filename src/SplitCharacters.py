#This code constructs new characters out of the characters in an 
#existing FlorML data matrix. It uses predefined categories to make new 
#characters. The input files are a tsv file containing the  data matrix, 
#and a file containing for each category the category on one line, 
#ending with ":", and the states belonging to that category on next 
#line. The output is a new matrix (matrix.tsv) with the characters 
#splitted.

import sys
import re

import table


matrixFile = open(sys.argv[1], 'r')
termsAndCategories = open(sys.argv[2], 'r')

matrix = []


def addNewValue(array, regexes):
	#Adds the correct terms to new columns made in the matrix
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
		termsList = termList.sort()
		terms = ','.join(termList)

		if terms == '':
			terms = '-'

		newArray[i] = terms

	return newArray



def splitColumns(matrix, term, regexes):
	#Looks for a regular expression in one of the columns of a matrix. When 
	#found, a new column is made with new term added to the hierarchy were 
	#it belongs.
	lastTerm = ''
	newTerm = ''

	for array in matrix[1:]:
		if array[0] == newTerm:
			continue

		for i in range(1, len(array)):
			if array[0] == lastTerm:
				break
				
			for regex in regexes:

				if re.search(regex, array[i]):
					lastTerm = array[0]
					newTerm = '/'.join([array[0], term.lower()])	
					newArray = addNewValue(array, regexes)
					newArray[0] = newTerm

					matrix.insert(matrix.index(array) + 1, newArray)
					break	
	return matrix

 
def markOriginalCharacters(matrix):
	#This function marks the original characters with "*", because
	#some of the categories were already a character, which causes 
	#problems in the code that must recognize some characters.
	for row in matrix[1:]:
		markedOriginalTerm = row[0] + '*'
		row[0] = markedOriginalTerm

	print 'original categories marked'
	return matrix
		


def initSplitting(termsAndCategories, matrix):
	#Adds new characters to the matrix	
	markOriginalCharacters(matrix)

	for line in termsAndCategories:

		if line.endswith(':\n'):
			term = line[:len(line) - 2]
			print line
		if len(line.split(',')) > 1:
			regexes = line[:len(line) - 1].split(',')

			splitColumns(matrix, term, regexes)
	return matrix


def deleteRowsAlmostEmpty(matrix):
	#This function deleted the rows from the matrix, that with less 
	#than 10 cells filled
	result = matrix[:]
	
	for row in matrix:

		if len(list(set(row[1:]))) < 10:			
			result.remove(row)
	return result


matrix = table.readMatrix(matrixFile)
print 'matrix read'
matrix = map(list, zip(*matrix))			

matrix = deleteRowsAlmostEmpty(matrix)
print 'Almost empty rows deleted'
matrix = initSplitting(termsAndCategories, matrix)
decodeWholeMatrix(matrix)
table.printToTsv(map(list, zip(*matrix)))

print 'columns splitted'

