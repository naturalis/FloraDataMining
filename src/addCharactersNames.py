import sys
import re

matrixFile = open(sys.argv[1], "r")
termsAndRegex = open(sys.argv[2], "r")
termsAndClasses = open(sys.argv[3], "r")
matrix = []
output = open("matrix.tsv", "w")
colourList = ['aquamarine', 'azure', 'black', 'blu', 'brown', 'champagne', 'crimson' , 'cyan' , 'gold', 'green', 'grey', 'indigo', 'lavender', 'lilac', 'magenta', 'maroon', 'orang', 'pink', 'purpl',  'red', 'scarlet', 'silver', 'transparent', 'turquoise', 'variously colored', 'vermillion', 'violet', 'whit', 'yellow']


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

 
def initSplitting(termsAndRegex, matrix):		
	for line in termsAndRegex:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2]
		if line[0] == "(":
			regex = line[:len(line) - 1]
			splitColumns(matrix, term, regex)


def countClasses(matrix):
	for j in range(1, len(matrix[0])):
		tempRow = []
		count = 0
		for i in range(1, len(matrix)):
			tempRow.append(matrix[i][j])	
		for string in tempRow:
			if string != "-":
				count += 1		
		set = {}
  		map(set.__setitem__, tempRow, [])
		print matrix[0][j]
		print len(set.keys()) 
	
	
def categorizeOrdinals(array, classes):
	orderArray = [0 for i in range(len(array))]
	classNumber = 0
	for string in classes:
		classNumber += 1
		for i in range(len(array)):			
			if string in array[i].split(",")[0]: 
				orderArray[i] = classNumber
	return orderArray


def categorizeRange(string):
	numberRange = re.match('[0-9]+-[0-9]+', string).group(0)
	numbers = numberRange.split('-')
	lowest = numbers[0]
	highest = numbers[1]
	return highest	


def categorizeNumerics(array):
	print array
	for i in range(len(array)):
		if re.match('[0-9]+-[0-9]+', array[i]):
			array[i] = categorizeRange(array[i])
		elif re.match('[0-9]+(?:/.[0-9]+|)', array[i]):
			numbers = re.findall('[0-9]+', array[i])
			array[i] = int(numbers[len(numbers) - 1])
	return array


def initCategorization(matrix, term, termList):
	tMatrix = map(list, zip(*matrix))

	for i in range(1, len(tMatrix)):
		classes = tMatrix[i][0].split("/")

		if classes[len(classes)-1] == term:
			tMatrix[i][1:] = categorizeOrdinals(tMatrix[i][1:], termList)	
		elif all(isinstance(item, str) for item in tMatrix[i]) == True:
			tMatrix[i][1:] = categorizeNumerics(tMatrix[i][1:])
	return  map(list, zip(*tMatrix))


def readTermsAndClasses(termsAndClasses, matrix):
	for line in termsAndClasses:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2].lower()
		elif re.match('\w', line[0]):	
			classList = line[:len(line) - 1].split(",")
			matrix = initCategorization(matrix, term, classList)
	return matrix


for line in matrixFile:
	row = line.split("\t")
	matrix.append(row)

newMatrix = readTermsAndClasses(termsAndClasses, matrix)	
print newMatrix		
printMatrixToTsv(newMatrix)

