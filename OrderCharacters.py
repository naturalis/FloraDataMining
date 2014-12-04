#This program constructs a matrix with the features belonging to different plant species. 
#At the moment only the features are looked for and printed. However, these must be put in the matrix. 

import sys
import xml.etree.ElementTree as ET

tree = ET.parse("A24_Piperaceae3.xml")
characterFile = open("selection_of_characters_Pip.csv", "r")
root = tree.getroot()
numberOfFeatures = 0


def printToCsv(matrix):	
	for i in range(len(matrix)):
		line = ""
		for j in range(len(matrix[0])):
			line = line + str(matrix[i][j]) + ","	
		print line 


def fillMatrix(matrix):
	for taxon in root.findall("./treatment/taxon"):
		for name in taxon.findall('//name'): 
			if name.text == matrix[i][0]:
				for character in taxon.finall('char'):
					print character


def getCharacters(matrix, chars):
	i = 0
	for line in chars:
		char = line.split(",")[1]
		if line.split(",")[2] == "Y":
			i+=1
			matrix[0][i] = char	


def getSpecies(matrix):	
	i = 0
	for nomenclature in root.findall("./treatment/taxon/nomenclature"):		
		homotypes = nomenclature[0]
		if homotypes[0].get('class') == 'accepted':
			genus = ""
			subspecies = ""
			variety = ""
			infrank = ""
			species = ""
			for name in homotypes.findall('.//name'): 				
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
			if genus == "Piper" or genus == "Peperomia":
				i+=1	
				matrix[i][0] = genus + " " + species + " " + infrank + variety + subspecies
				print matrix[i][0]
			

def getNumberOfCharacters(char):
	numberOfChar = 0
	for line in char:
		if line.split(",")[2] == "Y":
			numberOfChar+=1
	char.seek(0)
	return numberOfChar


def getNumberOfSpecies():
	numberOfSpecies = 0
	for homotypes in root.findall("./treatment/taxon/nomenclature/homotypes"):		
		for nom in homotypes:
			if nom.get('class') == 'accepted':
				for name in homotypes.findall('.//name'):
					if name.text == "Piper" or name.text == "Peperomia":					
						numberOfSpecies += 1
	return numberOfSpecies


numberOfCharacters = getNumberOfCharacters(characterFile)
numberOfSpecies = getNumberOfSpecies()
matrix = [[0 for i in range(numberOfCharacters + 1)] for j in range(numberOfSpecies + 1)]
getSpecies(matrix)
getCharacters(matrix, characterFile)
printToCsv(matrix)				
					

					
				

			

			
