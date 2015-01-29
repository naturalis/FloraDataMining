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


def categorizeFloat(string):
	number =  float(re.search('[0-9]+\.[0-9]+', string).group(0))
	return int(number) + 1


def categorizeRange(string):
	numberRange = re.search('[0-9]+-[0-9]+', string).group(0)
	numbers = numberRange.split('-')
	lowest = numbers[0]
	highest = numbers[1]
	return highest	


def categorizeFloatRange(string):
	match = re.search('[0-9]-[0-9]+\.[0-9]+', string).group(0)
	number = float(match[2:])
	return int(number) + 1


def categorizeNumerics(array):

	for i in range(len(array)):
		if array[i] == '-':
			array[i] = 0
		elif re.search('[0-9]-[0-9]+\.[0-9]+', array[i]):
			array[i] = categorizeFloatRange(array[i])
		elif re.search('[0-9]+-[0-9]+', array[i]):
			array[i] = categorizeRange(array[i])
		elif re.search('[0-9]+\.[0-9]+', array[i]):
			array[i] = categorizeFloat(array[i])
		elif re.search('[0-9]+', array[i]):
			number = re.search('[0-9]+', array[i]).group(0)
			array[i] = int(number)
	return array


#This code reads a matrix, a term, and a list with categories belonging to that term. It returns a matrix with integers corresponding to a category to which the values int he matrix are assigned.
def initCategorizationOrdinals(matrix, term, termList):
		
	for i in range(1, len(matrix)):
		classes = matrix[i][0].split("/")

		if classes[len(classes)-1] == term:
			matrix[i][1:] = categorizeOrdinals(matrix[i][1:], termList)
	return matrix
	

def initCategorizationNumerics(matrix):
	for i in range(1, len(matrix)):	
		if all(isinstance(item, str) for item in matrix[i]) == True:
			matrix[i][1:] = categorizeNumerics(matrix[i][1:])
			print matrix[i][0]
			if matrix[i][0] == '/habitat/altitude':
				for j in range(len(matrix[i])):

					if matrix[i][j] % 1000 == 0:
						matrix[i][j] = matrix[i][j]/1000 
		 			else:
						matrix[i][j]= matrix[i][j]/1000 + 1
			
	return matrix

	
#This code reads the file containing the terms and the different class assigned to that term. The term is put on the first row aneding wiht a :. IN the next line a row with classes is shown.
def readTermsAndClasses(termsAndCategories, matrix):
	

	for line in termsAndCategories:
		if line[len(line) - 2] == ":":
			term = line[:len(line) - 2].lower()
		elif re.match('\w', line[0]):	
			categoryList = line[:len(line) - 1].split(",")
			#When one term and its classes are found categorization of the text in the matrix with the help of the classses can start.
			matrix = initCategorizationOrdinals(matrix, term, categoryList)

	return matrix


for line in matrixFile:
	row = line.split("\t")
	matrix.append(row)
matrix = map(list, zip(*matrix))
matrix = readTermsAndClasses(termsAndClasses, matrix)
matrix = initCategorizationNumerics(matrix)

printMatrixToTsv(map(list, zip(*matrix)))

