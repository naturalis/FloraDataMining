import sys

characterFile = open(sys.argv[1], "r")
output = open("char_list.txt", "w")

for line in characterFile:
	if line.split(",")[2] == "Y":
	output.write(line.split(",")[1])
