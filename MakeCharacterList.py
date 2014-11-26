import xml.etree.ElementTree as ET
tree = ET.parse("A24_final.xml")
root = tree .getroot()

treatment = root[1]
taxon = treatment[0]
feature = taxon[2]

for taxon in treatment:
	print treatment.attrib

#taxon = feature[0]
#for feature in root.findall("./treatment/taxon"): 
#	print feature.attrib


