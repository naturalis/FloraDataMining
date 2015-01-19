import sys
import re

matrixFile = open(sys.argv[1], "r")
matrix = []
output = open("matrix.tsv", "w")
regex = '(?:bright(?:er|) |dark(?:er|) |dull(?:er|)|light(?:er|) |pale(?:r|) |pastel |waxy |)(?:aquamarine|azure|black(?:ish|)|blu(?:e|ish)|brown(?:ish|)|champagne|crimson|cyan|gold(?:en|ish|)|green(?:ish|)|grey(?:ish|)|indigo|lavender|lilac|magenta|maroon|orang(?:e|ish)|pink(?:ish|)|purpl(?:e|ish)|(?:brick |wine-|)red(?:dish|)|scarlet|silver(?:ish|)|transparent|turquoise|variously colored|vermillion|violet|whit(?:e|ish)|yellow(?:ish|))'


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


for line in matrixFile:
	row = line.split("\t")
	matrix.append(row)

i = matrix[0].index("/leaves/blade") + 1
matrix[0].insert(i, "/leaves/blade/colour")  


def addNewValue(matrix, i, regex):
	for j in range(1, len(matrix)):
		if re.search(regex, matrix[j][i - 1]):
			colour = re.search(regex, matrix[j][i - 1]).group(0)
			matrix[j].insert(i, colour)
		else:
			matrix[j].insert(i, "-")


for i in range(len(matrix)):
	for j in range(1, len(matrix[i])):
		if re.search(regex, matrix[i][j]):
			matrix[0].insert(j + 1, matrix[i][j] + "/colour")
			addNewValue(matrix, j, regex)
			break



	
printMatrixToTsv(matrix)
