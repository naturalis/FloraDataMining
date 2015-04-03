import sys
import table
import re

matrixFile = open(sys.argv[1], 'r')

def correctCharName(name):
	chars = name.split('/')

	if chars[len(chars) - 1] == chars[len(chars) - 2].split('*'):
		chars[len(chars) - 2] = chars[len(chars) - 2].split('*')[0]

	return '/'.join(chars[:len(chars)])


def clean(matrix):
	result = matrix[:]

	for row in matrix:

		if len(row[0]) != '-*' and len(row[0]) > 0:
			print row[0]
			if row[0][len(row[0]) - 1] == '*': 
				result.remove(row)

			elif re.search('length$', row[0]) or re.search('width$', row[0]):

				if matrix[matrix.index(row)][0] == matrix[matrix.index(row) + 1][0]:	
					result.remove(row)			

			elif row[0][len(row[0]) - 1] != '*':
				result[result.index(row)][0] = correctCharName(result[result.index(row)][0])
	
			row[0].replace('*', '')	
	return result


matrix = table.readMatrix(matrixFile)
matrix = clean(map(list, zip(*matrix)))

table.printToTsv(map(list, zip(*matrix)))
