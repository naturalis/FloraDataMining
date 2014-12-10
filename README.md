FloraDataMining
===============

What is the project about?

Plants species can be found with the help of traits, by a book called Flora. These Flora's are digitalized with XML to make this process easier. To find correlations between the different feature types in in Flora of the Guianas, a matrix must be developed with species on one axis and the relevant features on the other axis.

How does it work technically?

All terms will be parsed with the help of Python and ordered in a text file. The ontology of the Piperaceae is digitalized in A24_Piperaceae3.xml. The python script MakeCharacterList.py made a list of all characters in this file. The relevant characters were selected. These selections are shown in selection_of_characters_Pip.csv. The python script OrderCharacters.py constructs a matrix with the species and the characters. This matrix is displayed in a tab-delimited file: Piperaceae.tsv.

The input files are a FlorML file, and a csv file containing the characters in the FlorML file where the relevant characters are selected with "Y". 

What are the dependencies?

How can it be run?

A python script is written. The python script runs with the XML file as input. 
