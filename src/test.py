import re
from Length import Length

row = ["ca. 0.8-1 mm long", "ca. 0.3 mm long", "1 m long", "0.4-2.5 m long", "1-2.5 mm long"] 
amountUnits = {"mm": 0, "cm": 0, "dm": 0, "m": 0}

def normalize(row, units, correctUnit):
	numberRegex = '\d+\.*\d*'

	for cell in row:

		for unit in units:
	
			if re.search(" " + unit + "( |$)", cell):

				for number in re.findall(numberRegex, cell):
					value = Length(float(number), unit)
					correctedNumber = value.toUnit(correctUnit)[0]
					cell = cell.replace(number, str(correctedNumber))
	
				result = cell.replace(unit, correctUnit)


def selectDominatingUnit(amountUnits):

	for key, value in amountUnits.items():

		if value == max(amountUnits.values()):	
			return key


def countUnitNumbers(row, units):

	for cell in row:

		for key in amountUnits.keys():
	
			if re.search(" " + key + "( |$)", cell):
				units[key] += 1
	return units


countUnitNumbers(row, amountUnits)
print amountUnits
correctUnit = selectDominatingUnit(amountUnits)
row = normalize(row,amountUnits.keys(), correctUnit) 	


	

		
			

