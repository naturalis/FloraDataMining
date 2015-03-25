#This code corrects texts in an FlorML XML file, that are displayed between /subChar elements. This code puts these texts in the correct element. 

import xml.etree.ElementTree as ET
import sys
import re


flormlFile = open(sys.argv[1], 'r')
output = open("ordened.xml", 'w')
subCharacter = '<\/subChar>[,:] [a-z]'
misplacedCharacter = '<\/subChar>[,:] [^<]+'


for line in flormlFile:	

	if re.search(subCharacter, line):
		misplaced = re.findall(misplacedCharacter, line)
		fields = re.split('[<>]', line)

		for group in misplaced:
			fields[2] += "|" + group.split('>')[1]			

		line = fields[0] + "<"

		for i in range(1, len(fields) - 1):

			if i%2 == 0:
				line += fields[i] + "<"
			else:
				line += fields[i] + ">"		
	output.write(line)
