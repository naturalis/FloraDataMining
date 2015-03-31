import sys

file = open(sys.argv[1], "r")

lineNumber = 0

for line in file:
	
	if lineNumber == 63:
		print line
		print line[205]
	lineNumber += 1
	
