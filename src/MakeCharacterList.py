import xml.dom.minidom
import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()


def constructHierarchy(character, path):
	path = path + "/" + character.get('class')

	print path

	if character.getchildren():

		for child in character.getchildren():
		
			if child.get('class') != None:
				constructHierarchy(child, path)
	

			
for feature in root.findall("./treatment/taxon/feature"):

	for child in feature.getchildren():

		if child.get('class') != None:
			constructHierarchy(child, "")
