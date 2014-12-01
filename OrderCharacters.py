#This program constructs a matrix with the features belonging to different plant species. 
#At the moment only the features are looked for and printed. However, these must be put in the matrix. 

import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])
root = tree.getroot()
out = open("Flora_Matrix.txt", "w") 
numberOfFeatures = 1


def getSpecies(matrix):		
	for homotype in root.findall("./treatment/taxon/nomenclature/homotypes"):
		print homotype.get('class')
		if homotype.get('class') == 'accepted':
			for nameType in ('nameType'):	
				i = 0
				for child in nameType.getchildren():
					print child.get('class')

					for grandchild in child.getchildren():
						print child.get('class')
						i = i + 1
						if grandchild.get('class') == "genus abbreviation":
							genus = grandchild.text
						elif grandchild.get('class') == "species":
							species = grandchild.text
					for i in range(len(matrix)):
						matrix[i][0] = genus + " " + species
				
	
def getNumberOfSpecies():
	numberOfSpecies = 1
	for homotype in root.findall("./treatment/taxon/nomenclature/homotypes"):
		for child in homotype.getchildren():
			if child.get('class') == "accepted":
				for grandchild in child.getchildren():
					numberOfSpecies = numberOfSpecies + 1
	return numberOfSpecies


numberOfSpecies = getNumberOfSpecies()
matrix = [[0 for i in range(numberOfSpecies)] for j in range(numberOfFeatures)]

getSpecies(matrix)

print matrix[0][0]				
					

					
				

			

			
