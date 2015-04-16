#This function removes the columns from the FlorML matrices which are not 
#Needed for the analysis. It also makes the names of the characters easier
#to interpret.

import sys
import re

import table

matrixFile = open(sys.argv[1], 'r')

def correctCharName(name):
	#This function reads a character name and removes the nunneeded 
	#parts of it.
	if '*' in name:
		name = name.replace('*', '')

	chars = name.split('/')

	if chars[len(chars) - 1] == chars[len(chars) - 2]:
		chars[len(chars) - 2] = chars[len(chars) - 1]
		chars.pop()

	result = '/'.join(chars)


	return result


def clean(matrix):
	#This function removes superfluous columns and selects the columns 
	#that need to be saved to modify the character name. 
	result = matrix[:]
	
	for row in matrix:
		if len(row[0]) != '-*' and len(row[0]) > 0:
			if row[0].endswith('*'): 
				result.remove(row)

			elif re.search('length$', row[0]) or re.search('width$', row[0]):
				if matrix[matrix.index(row)][0] == matrix[matrix.index(row) + 1][0]:	
					result.remove(row)			

			else:
				result[result.index(row)][0] = correctCharName(result[result.index(row)][0])

	return result


matrix = table.readMatrix(matrixFile)
matrix = clean(map(list, zip(*matrix)))

table.printToTsv(map(list, zip(*matrix)))
