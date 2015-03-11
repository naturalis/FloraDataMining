
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


# This code converts a file containing a matrix to a double array.
def readMatrix(matrix, matrixFile):
	matrix = []

	for line in matrixFile:
		row = line.split("\t")

		matrix.append(row)		

	return matrix
