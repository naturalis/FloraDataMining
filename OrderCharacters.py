#This program constructs a matrix with the features belonging to different plant species. The arguments are a FlorML file, a csv file containing a table with the characters and a "Y", when they can be selected. The output is a tsv file containing the matrix.

import sys
import xml.etree.ElementTree as ET
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
tree = ET.parse(sys.argv[1])
characterFile = open(sys.argv[2], "r")
output = open("matrix.tsv", "w")
root = tree.getroot()
numberOfFeatures = 0

# This function prints the matrix in tsv format
def printToTsv(matrix):	
	for i in range(len(matrix)):
		line = ""
		for j in range(len(matrix[0])):
			line = line + str(matrix[i][j]) + "\t".strip('\n')	
		output.write(line)		


#This function prints the matrix in csv format						
def printToCsv(matrix):	
	for i in range(len(matrix)):
		line = ""
		for j in range(len(matrix[0])):
			line = line + str(matrix[i][j]) + ",".encode('utf-8')			
		print line


#This recursively adds the texts from the subcharacters to the matrix containing the text parst of the characters 
def addSubchars(matrix, char, name, i):
	if char.getchildren():
		for subchar in char.getchildren():
			newName = name + "/" + str(subchar.get('class'))
			
			for j in range(len(matrix[0])):			
				if  matrix[0][j] == newName:
					matrix[i][j] = subchar.text
					

			addSubchars(matrix, subchar, newName, i)


#This function fills the matrix with all descriptions of the characters.
def fillMatrix(matrix):
	i = 0
	j = 0
	for taxon in root.findall("./treatment/taxon"):		
		if taxon[0].tag	== "nomenclature":
			homotypes = taxon[0][0]
			if homotypes[0].get('class') == 'accepted':
				i+=1
				for child in taxon:
					if child.tag == "feature" and child.get('class') == "description":	
						for j in range(len(matrix[0])):
							for char in child:
								if matrix[0][j] == "/" + str(char.get('class')):
									matrix[i][j] = char.text
								addSubchars(matrix, char, "/" + str(char.get('class')), i)			
									

#This function extracts the relevant characters and puts them in the matrix
def getCharacters(matrix, chars):
	i = 0
	for line in chars:
		char = line.split(",")[1]
		if line.split(",")[2] == "Y":
			i+=1
			matrix[0][i] = char	


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
			

def getNumberOfCharacters(char):
	numberOfChar = 0
	for line in char:
		if line.split(",")[2] == "Y":
			numberOfChar+=1
	char.seek(0)
	print numberOfChar
	return numberOfChar


def getNumberOfSpecies():
	numberOfSpecies = 0
	for homotypes in root.findall("./treatment/taxon/nomenclature/homotypes"):		
		for nom in homotypes:
			if nom.get('class') == 'accepted':
				numberOfSpecies += 1
	return numberOfSpecies


numberOfCharacters = getNumberOfCharacters(characterFile)
numberOfSpecies = getNumberOfSpecies()
matrix = [["-" for i in range(numberOfCharacters + 1)] for j in range(numberOfSpecies + 1)]
getSpecies(matrix)
getCharacters(matrix, characterFile)
fillMatrix(matrix)
printToTsv(matrix)				
output.close()					

					
				

			

			
