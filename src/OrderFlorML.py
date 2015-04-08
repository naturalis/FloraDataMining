#This code corrects texts in an FlorML XML file, that are displayed between /subChar elements. This code puts these texts in the correct element. 

import xml.etree.ElementTree as ET
import sys
import re

flormlFile = open(sys.argv[1], 'r')
#characterFile = open(sys.argv[2], 'r')
output = open("ordened.xml", 'w')
subCharacter = '<\/subChar>[,:] [a-z]'
misplacedCharacter = '<\/subChar>[,:] [^<]+'
element = False
temp = []


def constructXmlLine(textList):
	result = "<"
	
	for i in range(1, len(textList) - 1):
		
		if i % 2 == 0:
			result += textList[i] + "<"
		else:
			result += textList[i] + ">"
	print '*' +  result
	return result


for line in flormlFile:
	startTag = "<char"
	endTag = "</char>"

	if startTag in line:
		element = True
		fields = re.split('[<>]', line)

	if element == False:
		output.write(line)

	if element == True:
		misplacedTexts = re.findall(misplacedCharacter, line)
		
		for text in misplacedTexts:
			fields[2] += "|" + text.split('>')[1]

		if startTag not in line:
			temp.append(line)

		if endTag in line:
			element = False

			output.write(constructXmlLine(fields))
			
			for textLine in temp:
				output.write(textLine)
			temp = []


#	if startTags and endTags:		
#		element += line
		
#		if len(startTags) == len(endTags):

#			if re.search(subCharacter, element):
#				misplacedTexts = re.findall(misplacedCharacter, element)
#				fields = re.split('[<>]', element)
	
#				for group in misplacedTexts:
		
#					fields[2] += "|" + group.split('>')[1]			

#				element = fields[0] + "<"
	
#				for i in range(1, len(fields) - 1):

#					if i%2 == 0:
#						element += fields[i] + "<"
#					else:
#						element += fields[i] + ">"	
#			output.write(element)
#			element = ""

#	elif not startTags and not endTags:
#		output.write(line)
