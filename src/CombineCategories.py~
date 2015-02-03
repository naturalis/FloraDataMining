import sys
import re

categoryFile = open(sys.argv[1], "r")
output = open("out.txt", "w")

def combineCategories(categoryList):

	for line in categoryList:

		if re.match('\w', line[0]):	
			categoryListLine = line[:len(line) - 1].split(",")
			newLine = ""
			print categoryListLine
			for i in range(len(categoryListLine)):
				for j in range(len(categoryListLine)):
					if i != j: 
						newLine += categoryList[i] + "," + categoryList[i] + " to " + categoryList[j] + "," + categoryList[i] + " or " + categoryList[j]
				if i != len(categoryListLine) - 1:
					newLine += ','
			line = newLine

		output.write(line)
		output.write("\n")

		
combineCategories(categoryFile) 
