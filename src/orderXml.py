import xml.etree.ElementTree as ET
import sys

xmlFile = open(sys.argv[1], 'r')
output = open("ordened.xml", 'w')

for line in xmlFile:
	fields = line.split("subChar")
		
	if len(fields) > 1:
		if fields[len(fields) - 1] != "</char>":
			print fields[len(fields) - 1]
			fields[0] = fields[0] + fields[len(fields) - 1]
			line = ""
			for field in fields:
				line+=field	
	output.write(line)
