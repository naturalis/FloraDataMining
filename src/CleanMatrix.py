import sys
import table

matrixFile = open(sys.argv[1], 'r')


def clean(matrix):
	newMatrix = matrix[:]

	for row in matrix:

		if len(row[0]) > 0:

			if row[0][len(row[0])-1] == '*' and row[0] != '-*' and len(row[0]) > 0:

				newMatrix.remove(row)

	return newMatrix


matrix = table.readMatrix(matrixFile)
matrix = clean(map(list, zip(*matrix)))

table.printToTsv(map(list, zip(*matrix)))
