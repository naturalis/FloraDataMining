import sys
import re

categoryFile = open(sys.argv[1], "r")
output = open("out.txt", "w")

def combineCategories(categoryList):

	for line in categoryList:
		if len(line[:len(line) - 1].split(",")) > 1:	
			categoryListLine = line[:len(line) - 1].split(",")
			newLine = ""			
			for i in range(len(categoryListLine)):
				newLine += categoryListLine[i]
				
				for j in range(len(categoryListLine)):
					if i != j: 
						newLine += ',' + categoryListLine[i] + " to " + categoryListLine[j] + "," + categoryListLine[i] + " or " + categoryListLine[j] 
					if j == len(categoryListLine) - 1:
						newLine += ','
			line = newLine
		else:
			print line
		print len(line.split(','))
		output.write(line)
		output.write("\n")
		
combineCategories(categoryFile) 
