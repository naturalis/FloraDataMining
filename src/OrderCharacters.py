#This program constructs a matrix with the features belonging to different plant species. The arguments are a FlorML file, a csv file containing a table with the characters and a "Y", when they can be selected. The output is a tsv file containing the matrix.

import sys
import xml.etree.ElementTree as ET
import codecs
import numpy
import matrix
import table

tree = ET.parse(sys.argv[1])
characterFile = open(sys.argv[2], "r")
root = tree.getroot()
#numberOfFeatures = 0


#In this function, all places in a matrix with "-" are counted. When this amount exceeds a [articular value, the corresponding row will be deleted. The argument are the matrix and the row number.
def countAndRemoveEmptyPlaces(matrix, i):
	emptyPlaces = 0

	for j in range(len(matrix[i])):

		if matrix[i][j] == "-":
			emptyPlaces += 1

	if emptyPlaces > len(matrix[0]) - 5:

		matrix = numpy.delete(matrix, i, axis = 0)

		if i != len(matrix):
			matrix = countAndRemoveEmptyPlaces(matrix, i)		
	return matrix


#In this fucntion a matrix is read and for each row not not containing enough values. The input is a matrix and the output is a smaller filtered matrix.
def deleteRowsLackingChars(matrix): 

	for i in range(len(matrix)):

		if i >= len(matrix) - 1:
			break

		else:
			if i != len(matrix):
				matrix = countAndRemoveEmptyPlaces(matrix, i)
	
	print "Empty places removed"						

	
#This recursively adds the texts from the subcharacters to the matrix containing the text parst of the characters 
def addSubchars(matrix, char, name, i):

	if char.getchildren(): 

		for  subchar in char.getchildren():
			newName = name + '/' + str(subchar.get('class'))
			
			for j in range(len(matrix[0])):
			
				if  matrix[0][j] == newName:

					if subchar.text:
						matrix[i][j] = subchar.text#.encode("UTF-8")
				
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
	

#This function adds the texts belonging to the subcharacters to the matrix.
def addChars(matrix, i, node):

	for j in range(len(matrix[0])):

		for char in node:

			if matrix[0][j] == "/" + str(char.get('class')) and char.text:
				matrix[i][j] = char.text

			addSubchars(matrix, char, "/" + str(char.get('class')), i)


#This function fills the matrix with all descriptions of the characters.
def fillMatrix(matrix):
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
							addChars(matrix, i, child)

							print "characters filled"
	
						elif child.get('class') == "habitat":
							addHabitatData(matrix, i, child)

							print "habitat data filled"
							


#This function reads characters and adds them to a matrix
def getCharacters(matrix, chars):
	i = 0

	for line in chars:
		i+=1
		matrix[0][i] = line.split("\n")[0]


#This function extracts the accepted family and species names and puts them in the matrix
def getSpecies(matrix):	
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
					
				matrix[i][0] = family + genus + " " + species + " " + infrank + variety + subspecies

				
#Counts the number of characters added to the matrix
def getNumberOfCharacters(char):
	numberOfChar = 0

	for line in char:
		numberOfChar+=1
	char.seek(0)

	return numberOfChar


#Counts the number of species in the matrix
def getNumberOfSpecies():
	numberOfSpecies = 0

	for homotypes in root.findall("./treatment/taxon/nomenclature/homotypes"):
		
		for nom in homotypes:

			if nom.get('class') == 'accepted':
				numberOfSpecies += 1
	return numberOfSpecies


numberOfCharacters = getNumberOfCharacters(characterFile)
numberOfSpecies = getNumberOfSpecies()
matrix = [["-" for i in range(2 + numberOfCharacters + 1)] for j in range(numberOfSpecies + 1)]
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
table.printToTsv(matrix)				

					
				

			

			
