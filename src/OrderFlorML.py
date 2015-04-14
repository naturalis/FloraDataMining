#This code searches in a FlorML file for text parts belonging to a 
#\char element, but which are wrongly placed between the \subchar 
#elements. The code copies these text parts to the correct place, with 
#a "|" on the places where text parts are pasted together. The input is a 
#FlorML file and the output is a new ordened FlorML file.
 
import sys
import re

import xml.etree.ElementTree as ET

MISPLACED_TEXT_REGEX = '<\/subChar>[,:] [^<]+'

flormlFile = open(sys.argv[1], 'r')
output = open('ordened.xml', 'w')
element = False
temp = []


def constructXmlLine(textList):
	#This function print a line in a FolroML file, which is splitted 
	#by "<" and ">" before
	result = '<'
	
	for i in range(1, len(textList) - 1):		
		if i % 2 == 0:
			result += textList[i] + '<'
		else:
			result += textList[i] + '>'
	return result


for line in flormlFile:
	startTag = '<char'
	endTag = '</char>'

	if startTag in line:
		element = True
		fields = re.split('[<>]', line)

	if not element:
		output.write(line)

	if element:
		misplacedTexts = re.findall(MISPLACED_TEXT_REGEX, line)
		
		for text in misplacedTexts:
			fields[2] += '|' + text.split('>')[1]

		if startTag not in line:
			temp.append(line)

		if endTag in line:
			element = False

			output.write(constructXmlLine(fields))
			
			for textLine in temp:
				output.write(textLine)
			temp = []


