import sys
import re

matrixFile = open(sys.argv[1], "r")
termsAndRegex = open(sys.argv[2], "r")
matrix = []
output = open("matrix.tsv", "w")

for line in matrixFile:
	row = line.split("\t")
	matrix.append(row) 


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


def addNewValue(matrix, i, regex):
	for j in range(1, len(matrix)):
		if re.search(regex, matrix[j][i - 1]):			
			termList = re.findall(regex, matrix[j][i - 1])
			terms = ','.join(termList)
			matrix[j].insert(i, terms)
		else:
			matrix[j].insert(i, "-")


def splitColumns(matrix, term, regex):
	lastTerm = ""

	for j in range(1, len(matrix[0])):
		for i in range(1, len(matrix)):					
			if re.search(regex, matrix[i][j]):
				if matrix[i][j] == lastTerm:
					break	
				else:
					matrix[0].insert(j + 1, matrix[0][j] + "/" + term.lower())
					addNewValue(matrix, j + 1, regex)
					lastTerm = matrix[i][j + 1]
					break

 
print len(matrix[0]) 			
for line in termsAndRegex:
	if line[len(line) - 2] == ":":
		term = line[:len(line) - 2]
	if line[0] == "(":
		regex = line[:len(line) - 1]
		splitColumns(matrix, term, regex)
print len(matrix[0]) 

printMatrixToTsv(matrix)
