import sys

characterFile = open(sys.argv[1], "r")

for line in characterFile:
	if line.split(",")[2] == "Y":
		print line.split(",")[1]
