import Flora
import OrderCharacters
import sys
#import xml.etree.ElementTree as ET
#import codecs
#import numpy

			
characterFile = open(sys.argv[2], "r")

numberOfCharacters = OrderCharacters.getNumberOfCharacters(characterFile)

numberOfSpecies = OrderCharacters.getNumberOfSpecies()

matrix = [["-" for i in range(2 + numberOfCharacters + 1)] for j in range(numberOfSpecies + 1)]

