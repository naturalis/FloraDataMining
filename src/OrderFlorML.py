#This code corrects texts in an FlorML XML file, that are displayed between /subChar elements. This code puts these texts in the correct element. 

import xml.etree.ElementTree as ET
import sys
import re

flormlFile = open(sys.argv[1], 'r')
output = open("ordened.xml", 'w')
subCharacter = '<\/subChar>[,:] [a-z]'
misplacedCharacter = '<\/subChar>[,:] [^<]+'
element = ""

for line in flormlFile:

	startTags = re.findall("<char|<subChar", line)
	endTags = re.findall("<\/char>|<\/subChar>", line)

	if startTags and endTags:		
		element += line
		
		if len(startTags) == len(endTags):

			if re.search(subCharacter, element):
				misplacedTexts = re.findall(misplacedCharacter, element)
				fields = re.split('[<>]', element)
	
				for group in misplacedTexts:
		
					fields[2] += "|" + group.split('>')[1]			

				element = fields[0] + "<"
	
				for i in range(1, len(fields) - 1):

					if i%2 == 0:
						element += fields[i] + "<"
					else:
						element += fields[i] + ">"	
			output.write(element)
			element = ""

	elif not startTags and not endTags:
		output.write(line)
