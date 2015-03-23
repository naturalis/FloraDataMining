import sys

file = open(sys.argv[1], "r")

lineNumber = 0

for line in file:
	
	if lineNumber == 3674:
		print len(line)
		print line[346]
	lineNumber += 1
	
