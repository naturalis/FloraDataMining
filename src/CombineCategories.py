import sys
import re

categoryFile = open(sys.argv[1], "r")
output = open("out.txt", "w")

def combineCategories(categoryList):

	for line in categoryList:

		if re.match('\w', line[0]):	
			categoryList = line[:len(line) - 1].split(",")
			newLine = ""

			for i in range(len(categoryList)):
				for j in range(len(categoryList)):
					if i != j: 
						newLine += categoryList[i] + "," + categoryList[i] + " to " + categoryList[j] + "," + categoryList[i] + " or " + categoryList[j]
					if i != len(categoryList) - 1:
						newLine += ','
			line = newLine

		output.write(line)
		output.write("\n")

		
combineCategories(categoryFile) 
