import xml.etree.ElementTree as ET
import sys
import re

xmlFile = open(sys.argv[1], 'r')
output = open("ordened.xml", 'w')

for line in xmlFile:
	if re.search('<\/subChar>, [a-z]', line) or re.search('<\/subChar>: [a-z]', line):
		print line
		fields = re.split(r'[<>]', line)		
		fields[2] = fields[2] + "|" + fields[6]
		line = fields[0] + "<"

		for i in range(1, len(fields) - 1):
			if i%2 == 0:
				line += fields[i] + "<"
			else:
				line += fields[i] + ">"
		print line		
	output.write(line)
