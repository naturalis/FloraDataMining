#This program constructs a matrix with the features belonging to different plant species. 
#At the moment only the features are looked for and printed. However, these must be put in the matrix. 

import sys
import xml.etree.ElementTree as ET

tree = ET.parse("A24_Piperaceae.xml")
characters = open("selection_of_characters_Pip.csv", "r")
root = tree.getroot()
numberOfFeatures = 0


def printToCsv(matrix):	
	for i in range(len(matrix)):
		line = ""
		for j in range(len(matrix[0])):
			line = line + str(matrix[i][j]) + ","	
		print line 


def getCharacters(matrix, chars):
	for line in chars:
		print line
		char = line.split(",")[0]
		print char
		if line.split(",")[2] == "Y":
			matrix[0][0] = char


def getSpecies(matrix):	
	i = 0
	for nomenclature in root.findall("./treatment/taxon/nomenclature"):		
		homotypes = nomenclature[0]
		if homotypes[0].get('class') == 'accepted':
			i+=1
			for name in homotypes.findall('.//name'):
				
				if name.get('class') == 'genus':
					genus = name.text
				elif name.get('class') == 'species':
					species = name.text
				
			matrix[i][0] = genus + " " + species
			

def getNumberOfCharacters(char):
	numberOfChar = 0
	for line in char:
		if line.split(",")[2] == "Y":
			numberOfChar+=1
	return numberOfChar


def getNumberOfSpecies():
	numberOfSpecies = 0
	for homotype in root.findall("./treatment/taxon/nomenclature/homotypes"):		
		for nom in homotype:
			if nom.get('class') == 'accepted':
				numberOfSpecies = numberOfSpecies + 1
	return numberOfSpecies


numberOfCharacters = getNumberOfCharacters(characters)
numberOfSpecies = getNumberOfSpecies()
matrix = [[0 for i in range(numberOfFeatures + 1)] for j in range(numberOfSpecies + 1)]
getSpecies(matrix)
getCharacters(matrix, characters)
				
					

					
				

			

			
