import sys

matrixFile = open(sys.argv[1], "r")
output = open("new_matrix.tsv", "w")

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


def fillByGenerus(matrix, generus):
	generus = generus.lower()

	for i in range(len(matrix)):
		if matrix[i][0].lower() == generus:
			rowValue = i
			break

		if generus in matrix[i][0].lower():
			for j in range(len(matrix)):
				if matrix[i][j] == 0:
					matrix[i][j] == matrix[rowValue][j]		


def fillByFamily(matrix):
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == "-":
				matrix[i][j] = matrix[1][j]


def readMatrix(matrix, matrixFile):
	for line in matrixFile:
		row = line.split("\t")
		matrix.append(row)
	return matrix


matrix = readMatrix([], matrixFile)

fillByGenerus(matrix, "Peperomia")
fillByGenerus(matrix, "Piper")
fillByFamily(matrix)
printMatrixToTsv(matrix)	



