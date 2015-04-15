output = open("matrix.tsv", "w")


# This function prints a matrix in tsv format, when giving the matrix as argument.
def printToTsv(table):

	for i in range(len(table)):
		line = ""	

		for j in range(len(table[0])):
			table[i][j] = str(table[i][j]).replace("\t", " ") 
			line = line + table[i][j] + "\t"
		
		line = line.replace("\n", "") 

		output.write(line)
		output.write("\n")


# This code converts a file containing a matrix to a double array.
def readMatrix(matrixFile):
	matrix = []

	for line in matrixFile:
		row = line.split("\t")

		matrix.append(row)		

	return matrix
