import xml.dom.minidom
import xml.etree.ElementTree as ET
tree = ET.parse("A24_final.xml")
root = tree.getroot()
path = "./treatment/taxon/feature//"

for character in root.findall(path):
	output = str(character.attrib)
	if character.hasChildNodes():
		
		if character.tag == "char" or character.tag == "subChar":
		children = character.getchildren()
		for child in children:
			print str(character.attrib) + "/"+ str(child.attrib) 

