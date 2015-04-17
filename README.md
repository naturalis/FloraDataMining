FloraDataMining
===============

Introduction
------------
Plant species can be determined with the help of books mentioned Floras. There are multiple types of plants and multiple types of Floras. When a botanist wants to determine a plant he must access the correct Flora. 
These Floras are digitalized in an XML format mentioned FlorML, which is recogizable for humans and for machines, to make them accessible by computer. The reason this digitalisation is not only the accessibility. When digitalized, the Flora data can be put into table form. Then, some tests can be performed with this table to find correlation between species and their traits (mentioned characters). During this project, the text in the FlorML file is converted to a table with plant species belonging to a articular Flora on one axis and relevant plant features (characters) on the other axis. 


The different steps in constructing the matrix
----------------------------------------------
This project is performed with Python 2.7.6. Together there are matrices constructed for six different FlorML files: A22_final.xml, A23_final.xml, A24_Piperaceae5.xml, A25_final2.xml, A26_final.xml, A27_final.xml

**Parsing the characters (MakeCharacterList.py FlorML file )**
First, a list was made containing all characters present in the FlorML file. With the help of such lists, it is possible to select characters relevant for the study by hand. Because sometimes the same name is used to define different character types, all characters are displayed together with their superiors, like “/grandparent/parent/current character”. These lists, constructed for six different FlorML files, are all saved in "results/character_lists".

**Ordering the text in the FlorML file (OrderFlorML.py FlorML file)**
Before continuing the matrix construction, the text in the FlorML files had to be ordened. The reason was that there were some structural incorrectnesses in the placement of some text parts in the FlorML file, where converting handwritten text to XML is comprehensive. Using this format, many text parts will not be displayed in the matrix. A code was written to put the texts displayed on the wrong place to the correct places. These new strcutued FlorML files are saved in results/ordened_FlorML.

**Organizing the text to a matrix (OrderCharacters.py (structured) 1.FlorML file 2.character list)**
A script was written to construct a matrix containing text parts belonging to species(rows) and characters(columns). The input files were a FlorML file, and a txt file including a list with relevant the characters. The output is a tab-delimited file containing the matrix. The rows represent the species and the columns represent the characters. In this table some characters contained such a small amount of information, that these were also removed by the script. These first versions od the matrices are saved in results/matrices, where all following versions of the matrices also are saved, starting with the name of the FlorMl version.

**Splitting of the characters (SplitColumns.py  1.tsv file containing matrix 2.term list)**
When the texts in the FlorML files were constructed to a matrix, many cells contained sentences which made it difficult to implement them in a data mining analysis. Because of this, a script is written to split some characters into some of the following child characters: colour, growth form, hairs, margin type, position, texture, shape, environment. So, the FlorML file did not contain these new characters, but they were determined by looking what the text in the matrix described. As input files the matrices constructed by OrderCharacters were used, with one exception. Instead of A24.xml_matrix.tsv, tsv file was used where some columns were removed by hand. This was done before the part of the script was written that removed columns with a small amount of filled columns. This file has the name condensed_matrix.tsv and is saved in data/CharacterSplitting. All matrices containing these new characters are saved under names starting with "newchars".

**Selecting terms to complete the term list (FindNewWords.py 1.tsv file containing matrix 2.term list DisplayAmountNewWords.py 3.list with common English words, DisplayAmountNewWords.py 1.tsv file containing matrix 2.term list DisplayAmountNewWords.py)**
The matrices are constructed with the help of a list of categories and terms. This term list is not complete at the moment. In every new matrix words are found that need to be added to the list. These words can be found with the python script FindNewWords.py. This reads data/terms_and_categories.txt and a tsv file of a matrix. 
The script DisplayAmountNewWords.py was made to construct result/fraction_new_words.pdf. This is a plot containing the fraction of new words. In this plot the order of the number of the matrices is used: A22 first and A27 last.

**Converting the nominal categories into bit strings (ConvertNamesToBit.py 1.tsv file containing matrix 2.term list)**
Every character for every species can contain multiple terms printed in the corresponding cell. For this reason, the nominal characters are converted into bit strings, displaying a 0 when a value is absent and a 1 when a value is present. These codes are based on all categories displayed in the current matrix. This means that NOT EVERY MATRIX CONSTRUCTED SEPARATELY CAN BE COMPARED TO EACH OTHER. These new matrices were saved under names starting with "bit".

**Organizing the numerical values (ClearNumerics tsv file containing matrix)**
Some characters contained multiple numerical values, in a range or in dimensions. These characters splitted into sub characters: length, width, minimum, maximum. This way they can be as numerical values in the data mining analysis. The outputs of this script are saved with a name staring with "num".

**Removing redundant information (CleanMatrix.py 1.tsv file containing matrix)**
During the development of the matrices many information was kept, because it is clear to other project members what the different scripts exactly do. However, because it is not easy to understand some parts, a script was written to remove redundant information. All columns that contain sentences instead of numbers, character states, or bit strings were removed. Strange names were also changed. Some categories were same as the name of some characters filtered of the FlorML file. This resulted them to be displayed twice in the matrix sometimes, and twice in a hierarchy. For example, if there was already a character with the name shape, the script SplitColumns.py still splits this into a new character with the name shape. The ones where the character name ends with a "*", are the not processed ones, and every character ending with a "*" is removed by this script. The tsv matrix files produced by this script are saved under a name starting with "final".


Description of the Python Scripts
---------------------------------
**Table.py**
This small module contains functions to work with tables or matrices in tsv format.

ConstructCharacterList.py
This script reads a FlorML file, and returns a list of all characters found in the FlorML file. The sub characters are displayed together with their parent characters in alphabetical order. 

**OrderFlorML.py**
This script searches in a FlorML file for text parts belonging to a \char element, but which are wrongly placed between the \subchar elements. The code copies these text parts to the correct place, with a "|" on the places where text parts are pasted together. The input is a FlorML file and the output is a new ordened FlorML file. 

**OrderCharacters.py**
This script constructs a matrix with the features belonging to different plant species. The arguments are a FlorML file, and a txt file containing important characters. The output is a tsv file 
(matrix.tsv) containing the matrix. The names off all species found in the matrix are printed while running the code. It also shows it when character data is added, and (when present) habitat data is added. Running this code takes some time, around 15 minutes for an average FlorML file.

**DisplayAmountNewTerms.py**
This code counts all words for a given matrix in a list. With this list and words that are new added the fraction of more used words in a new FlorML file is calculated. The Words in the first row and column are not included. The output is a plot showing a curve which shows the fraction of new words when reading a new file.

**FindNewTerms.py**
This code reads a matrix in tsv format and a list of categories and states used to split the matrix into more matrices. This code looks for words which are not yet included in the the list of categories and  terms, but should be included. Common used English words or words ending with a punctuation mark are excluded. The output shows how much words are found and a list of the 
new words. 

**SplitCharacters.py**
This script constructs new characters out of the characters in an existing FlorML data matrix. It uses predefined categories to make new characters. The input files are a tsv file containing the  data matrix, and a file containing for each category the category on one line, ending with ":", and the states belonging to that category on next line. The output is a new matrix (matrix.tsv) including more subcharacters.

**ConvertNominalsToBit.py** 
This script converts the states of a character to a bit string of all states present in the matrix: 1 means that the state is present for the current species and 0 means not present. This input is a data matrix in tsv format without bit values and the output is a data matrix (matrix.tsv) containing a new column displaying these bit strings. 

The bit values are first written to be printed in table form, where at the end the cells in a row were sticked together to form a string. The reason was that initially the idea was to print a matrix for every character, containing all states and species.

**ModifyNumerics.py**
This script modifies all numerical values in a data matrix. Dimensions values are divided in length and with, and ranges in minimum and maximum. New columns are constructed only displaying the numerical values for a character. Some modules of the library pyuom are used fir the unit conversion.

**CleanMatrix.py**
This function removes the columns from the FlorML matrices which are not needed for the analysis. It also makes the names of the characters easier to interpret.



