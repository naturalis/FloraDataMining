import xml.dom.minidom
import xml.etree.ElementTree as ET
tree = ET.parse("A24_Piperaceae.xml")
root = tree.getroot()


def constructHierarchy(character, path):
	path = path + "/" + character.get('class')

	if character.getchildren():

		for child in character.getchildren():
		
			if child.get('class') != None:
				constructHierarchy(child, path)

			
for feature in root.findall("./treatment/taxon/feature"):

	for child in feature.getchildren():

		if child.get('class') != None:
			constructHierarchy(child, "")
