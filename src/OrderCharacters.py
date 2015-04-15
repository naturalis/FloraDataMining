#This program constructs a matrix with the features belonging to 
#different plant species. The arguments are a FlorML file, and a txt 
#file containing important charactersThe output is a tsv file 
#(matrix.tsv) containing the matrix. The names off all species found in 
#the matrix are printed while running the code. It also shows it when 
#character data is added, and (when present) habitat data is added. 
#Running this code takes some time, around 15 minutes for an average 
#FlorML file.

import sys
import xml.etree.ElementTree as ET
import codecs
import numpy
import matrix
import table

tree = ET.parse(sys.argv[1])
characterFile = open(sys.argv[2], "r")
root = tree.getroot()


def decodeWholeMatrix(matrix):
	#This function reads all strings in a matrix and encodes UTF-8."

	for row in matrix:
		for i in range(len(row)):
			matrix[matrix.index(row)][i] = matrix[matrix.index(row)][i].encode('UTF-8')



def countAndRemoveEmptyPlaces(matrix, i):
	#In this function, all places in a matrix with "-" are counted. When 
	#this amount exceeds a particular value, the corresponding row will be 
	#deleted. The argument are the matrix and the row number.
	emptyPlaces = 0

	for j in range(len(matrix[i])):

		if matrix[i][j] == "-":
			emptyPlaces += 1

	if emptyPlaces > len(matrix[0]) - 5:

		matrix = numpy.delete(matrix, i, axis = 0)

		if i != len(matrix):
			matrix = countAndRemoveEmptyPlaces(matrix, i)		
	return matrix



def deleteRowsLackingChars(matrix): 
	#In this function a matrix is read and for each row notnot containing 
	#enough values. The input is a matrix and the output is a smaller 
	#filtered matrix.
	for i in range(len(matrix)):

		if i >= len(matrix) - 1:
			break

		else:
			if i != len(matrix):
				matrix = countAndRemoveEmptyPlaces(matrix, i)
	
	print "Empty places removed"						

	

def addSubchars(matrix, char, name, i):
	#This recursively adds the texts from the subcharacters to the matrix 
	#containing the text parts of the characters 
	if char.getchildren(): 

		for  subchar in char.getchildren():
			newName = '/'.join([name, str(subchar.get('class'))])
			
			for j in range(len(matrix[0])):
			
				if  matrix[0][j] == newName:

					if subchar.text:
						matrix[i][j] = subchar.text
				
			addSubchars(matrix, subchar, newName, i)
	

#Adds the habitat and its altitude to the matrix.
def addHabitatData(matrix, i, node):
	habitat = node.find('.//habitat')
	altitude = node.find('.//altitude')
	
	if altitude != None:

		if altitude.text:
			matrix[i][len(matrix[0]) - 1] = altitude.text
	if habitat != None:

		if habitat.text:
			matrix[i][len(matrix[0]) - 2] = habitat.text	
	


def addCharData(matrix, i, feature):
	#This function adds the texts belonging to the subcharacters to the 
	#matrix.
	for j in range(len(matrix[0])):

		for char in feature:

			if matrix[0][j] == "/"+str(char.get('class')) and char.text:
				matrix[i][j] = char.text

			addSubchars(matrix, char, "/"+str(char.get('class')), i)



def fillMatrix(matrix):
	#This function fills the matrix with all descriptions of the characters.
	i = 0

	for taxon in root.findall("./treatment/taxon"):	

		if taxon[0].tag	== "nomenclature":
			homotypes = taxon[0][0]

			if homotypes[0].get('class') == 'accepted':
				i+=1

				print matrix[i][0]

				for child in taxon:

					if child.tag == "feature":
 
						if child.get('class') == "description":
							addCharData(matrix, i, child)

							print "character data added"
	
						elif child.get('class') == "habitat":
							addHabitatData(matrix, i, child)

							print "habitat data added"
							


def getCharacters(matrix, chars):
	#This function reads characters and adds them to a matrix.
	i = 0

	for line in chars:
		i+=1
		matrix[0][i] = line.split("\n")[0]


def getSpecies(matrix):	
	#This function extracts the accepted family and species names and puts 
	#them into the matrix.
	i = 0

	for nomenclature in root.findall("./treatment/taxon/nomenclature"):		
		homotypes = nomenclature[0]

		if homotypes[0].get('class') == 'accepted':
			i+=1
			family = ""
			genus = ""
			subspecies = ""
			variety = ""
			infrank = ""
			species = ""

			for name in homotypes[0].findall('.//name'):

				if name.get('class') == 'family':
					family = name.text

				if name.get('class') == 'genus':
					genus = name.text

				elif name.get('class') == 'species':
					species = name.text

				elif name.get('class') == 'subspecies':
					subspecies = name.text

				elif name.get('class') == 'infrank':
					infrank = name.text

				elif name.get('class') == 'variety':
					variety = name.text
					
				matrix[i][0] = " ".join([family+genus, species, infrank+variety+subspecies])

				

def getNumberOfCharacters(char):
	#Counts the number of characters added to the matrix.
	numberOfChar = 0

	for line in char:
		numberOfChar+=1
	char.seek(0)

	return numberOfChar



def getNumberOfSpecies():
	#Counts the number of species in the matrix
	numberOfSpecies = 0

	for homotypes in root.findall("./treatment/taxon/nomenclature/homotypes"):
		
		for nom in homotypes:

			if nom.get('class') == 'accepted':
				numberOfSpecies += 1
	return numberOfSpecies


NUMBER_OF_CHARACTERS = getNumberOfCharacters(characterFile)
NUMBER_OF_SPECIES = getNumberOfSpecies()

matrix = [["-" for i in range(2 + NUMBER_OF_CHARACTERS + 1)] for j in 
range(NUMBER_OF_SPECIES + 1)]
matrix[0][len(matrix[0]) - 1] = "/habitat/altitude"
matrix[0][len(matrix[0]) - 2] = "/habitat"


getSpecies(matrix)
print  "species added"
getCharacters(matrix, characterFile)
print "characters added"
fillMatrix(matrix)
print "matrix filled" 
deleteRowsLackingChars(matrix)
print "rows lacking chars deleted"
decodeWholeMatrix(matrix)
table.printToTsv(matrix)				

					
				

			

			
