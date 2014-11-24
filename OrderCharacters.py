#This program constructs a matrix with the features belonging to different plant species. 
#At the moment only the features are looked for and printed. However, these must be put in the matrix. 

import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])
root = tree.getroot()
out = open("Flora_Matrix.txt", "w") 
numberOfSpecies = 0
numberOfFeatures = 0 

#Count the number of species
for feature in root.findall(".//*[@class='species']"):
	numberOfSpecies++ 
out.write("\n")

#Construct the table
table= [ [ 0 for i in range(numberOfSpecies) ] for j in range(numberoFFeatures) ]

for feature in root.findall(".//*[@class='species']"):
	out.write(feature.text + " ")
out.write("\n")

for feature in root.findall(".//*[@class='genus']"):
	out.write(feature.text + " ")	
out.write("\n")

for feature in root.findall(".//*[@class='habit']"):
	out.write(feature.text + " ")
out.write("\n")

for feature in root.findall(".//*[@class='distribution']"):
	out.write(feature.text + " ")
out.write("\n")

out.close()
