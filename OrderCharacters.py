#This program constructs a matrix with the features belonging to different plant species. 
#At the moment only the features are looked for and printed. However, these must be put in the matrix. 

import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])
root = tree.getroot()
out = open("Flora_Matrix.txt", "w") 
numberOfFeatures = 1


def printToCsv(matrix):
	line = ""
	for i in range( len(matrix)):
		for j in range( len(matrix[i] )):
			line = line + str(matrix[i][j]) + ","	
		print line


def getSpecies(matrix):	
	i = 0	
	for nomenclature in root.findall("./treatment/taxon/nomenclature"):
		
		homotypes = nomenclature[0]
		nametype = homotypes.find('nameType')
		print nametype.tag
		if homotypes.get('class') == 'accepted':
			i = i + 1
			genus = nomenclature[1][0].text
			species = nomeclature[1][1].text
			matrix[0][i] = genus + " " + species	
				
	
def getNumberOfSpecies():
	numberOfSpecies = 0
	for homotype in root.findall("./treatment/taxon/nomenclature/homotypes"):		
		for nom in homotype:
			if nom.get('class') == 'accepted':
				numberOfSpecies = numberOfSpecies + 1
	return numberOfSpecies


numberOfSpecies = getNumberOfSpecies()
matrix = [[0 for i in range(numberOfSpecies + 1)] for j in range(numberOfFeatures + 1)]
getSpecies(matrix)
printToCsv(matrix)				
					

					
				

			

			
