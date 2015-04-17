#This code reads a matrix in tsv format and a list of categories and states 
#used to split the matrix into more matrices. This code looks for words which 
#are not yet included in the the list of categories and  terms, but should 
#be included. Common used English words or words ending with a punctuation 
#mark are excluded. The output shows how much words are found and a list of 
#new words. 


import sys
import re
import table

matrixFile = file(sys.argv[1], 'r')
termList = file(sys.argv[2], 'r')
commonEnglishWordsFile = file(sys.argv[3], 'r')
commonEnglishWords = []
newTerms = []
matrix = table.readMatrix(matrixFile)

for line in commonEnglishWordsFile:
	
	commonEnglishWords.append(line.split('. ')[1].split('\n')[0])


for row in matrix[1:]:
	for cell in row[1:]:		
		for word in cell.split(' '):
			if len(word) > 1:
				if not word[len(word) - 1].isalpha():
					word = word[:len(word) - 1] 

				if word not in commonEnglishWords and re.match('[a-z]', word) and word not in newTerms and "," not in word:
					newTerms.append(word)

for line in termList:
	for term in line.split(','):
		for word in newTerms:
			if len(term) > 0 and re.match(term, word):				
				newTerms.remove(word)

					
print str(len(newTerms)) + " new terms"
print newTerms

