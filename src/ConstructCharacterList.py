#This code reads a FlorML file, and returns a list of all characters 
#found in the FlorML file. The sub characters are displayed together 
#with their parent characters in aplhabetical order.

import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET


tree = ET.parse(sys.argv[1])
root = tree.getroot()
characterList = []


def printCharacters():
	#This function removes duplicates from the list of characters 
	#and prints all characters in alphabetical order. 
	characterSet = set(characterList)
	chracaterList = list(characterSet).sort()

	for character in characterList:
		print character
	

def constructHierarchy(character, path):
	#This function reads a part of a character hierarchy in FlorML.
	#It constructs the hierarchy output and adds all characters 
	#and subcharacters to a list.
	path = '/'.join((path, character.get('class')))	
	characterList.append(path)

	if character.getchildren():
		for subcharacter in character.getchildren():
			if subcharacter.get('class'):
				constructHierarchy(subcharacter, path)

			
for feature in root.findall('./treatment/taxon/feature'):
	for character in feature.getchildren():
		if character.get('class'):
			constructHierarchy(character, '')
printCharacters()

