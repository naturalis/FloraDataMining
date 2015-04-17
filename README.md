FloraDataMining
===============

Introduction

Plant species can be determined with the help of books mentioned Floras. There are multiple types of plants and multiple types of Floras. When a botanist wants to determine a plant he must access the correct Flora. 
These Floras are digitalized in an XML format mentioned FlorML, which is recogizable for humans and for machines, to make them accessible by computer. The reason this digitalisation is not only the accessibility. When digitalized, the Flora data can be put into table form. Then, some tests can be performed with this table to find correlation between species and their traits (mentioned characters). 
During this project, the text in the FlorML file is converted to a table with plant species belonging to a articular Flora on one axis and relevant plant features (characters) on the other axis. This is performed with Python 2.7.6. Together there are matrices constrcuted for six different FlorML files: A22_final.xml, A23_final.xml, A24_final.xml, A25_final.xml, A26_final.xml, A27_final.xml

The different steps in constructing the matrix

Parsing the characters (MakeCharacterList.py FlorML file )
First, a list was made containing all characters present in the FlorML file. With the help of such lists, it is possible to select characters relevant for the study by hand. Because sometimes the same name is used to define different character types, all characters are displayed together with their superiors, like “/grandparent/parent/current character”. These lists, constructed for six different FlorML files, are all saved in "results/character_lists".

Ordering the text in the FlorML file (OrderFlorML.py FlorML file)
Before continuing the matrix construction, the text in the FlorML file ust be ordened. The reason is that there are some structural incorrectnesses in where some text parts are displayed in the FlorML file, where converting the text from a book to XML is comprehensive. In this format, many text parts will not be displayed in the matrix. Because of this, a code was written to put the texts displayed on the wrong place to the correct places.

Ordening the text to a matrix (OrderCharacters.py (structured) 1.FlorML file 2.character list
A code is written to construct a matrix containing values for species(rows) and characters(columns). The input files are a FlorML file, and a txt file including a list with relevant the characters. The output is a tab-delimited file containing the matrix. The rows represent the species and the columns represent the characters. In this table some characters contained not enough information. The corresponding columns were removed by hand. 

Looking for tersm which must be added to the character list (FindNewWords.py 1.tsv file containing matrix 2.term list DisplayAmountNewWords.py 3.list with common English words and DisplayAmountNewWords.py 1.tsv file containing matrix 2.term list DisplayAmountNewWords.py)
The matrices are constructed with the help of a list of categories and terms. These terms are not complete at the moment. In every new matrix words are found that need to be added to the list. These words can be found with the python script FindNewWords.py. This reads data/terms_and_categories.txt and a tsv file fo a matrix. 

The script DisplayAmountNewWords.py was use to construct result/fraction_new_words.pdf. This is a plot containing the fraction of new words. In this plot the order of the number of the matrices is used: A22 first and A27 last.

Splitting of the characters (SplitColumns.py  1.tsv file containing matrix 2.term list)
When the text in the FlorML file is constructed to a matrix, many fields in the table contain much text which makes it difficult to implement them in a data mining analysis. Because of this, a code is written to split some characters into some of the following child characters: colour, growth form, hairs, margin type, position, texture, shape, environment. So, the FlorML file did not contain these new characters, but they were determined by looking what the text in the matrix described.

Converting the nominal categories into bit strings (ConvertNamesToBit.py 1.tsv file containing matrix 2.term list)
Every character for every species can contain multiple categories. For this reason, the nominal characters must be converted into bit strings, displaying a 0 when a value is absent and a 1 when a value is present. These codes are based on all categories displayed in the current matrix. For  this reason, NOT EVERY MATRIX CONSTRUCTED SEPARATELY CAN BE COMPARED TO EACH OTHER.

Ordening the numerical values (ClearNumerics tsv file containing matrix)
For some characters there were multiple numerical values, in a range or in length and width for dimensions. Characters containing these values are splitted into the following child characters: length, width, minimum, maximum.


Descripion of the Python Scripts

Table.py
This small module contains functions to work with tables or matrices in tsv format.

ConstructCharacterList.py
This code reads a FlorML file, and returns a list of all characters found in the FlorML file. The sub characters are displayed together with their parent characters in alphabetical order. 

OrderFlorML.py
This code searches in a FlorML file for text parts belonging to a \char element, but which are wrongly placed between the \subchar elements. The code copies these text parts to the correct place, with a "|" on the places where text parts are pasted together. The input is a FlorML file and the output is a new ordened FlorML file. 

OrderCharacters.py
This program constructs a matrix with the features belonging to different plant species. The arguments are a FlorML file, and a txt file containing important characters. The output is a tsv file 
(matrix.tsv) containing the matrix. The names off all species found in the matrix are printed while running the code. It also shows it when character data is added, and (when present) habitat data is added. Running this code takes some time, around 15 minutes for an average FlorML file.

DisplayAmountNewTerms.py
This code counts all words for a given matrix in a list. With this list and words that are new added the fraction of more used words in a new FlorML file is calculated. The Words in the first row and column are not included. The output is a plot showing a curve which shows the fraction of new words when reading a new file.

FindNewTerms.py
This code reads a matrix in tsv format and a list of categories and states used to split the matrix into more matrices. This code looks for words which are not yet included in the the list of categories and  terms, but should be included. Common used English words or words ending with a punctuation mark are excluded. The output shows how much words are found and a list of 
new words. 

SplitCharacters.py
This code constructs new characters out of the characters in an existing FlorML data matrix. It uses predefined categories to make new characters. The input files are a tsv file containing the  data matrix, and a file containing for each category the category on one line, ending with ":", and the states belonging to that category on next line. The output is a new matrix (matrix.tsv) including more subchacaracters.

ConvertNominalsToBit.py 
This code converts the states of a character to a bit string of all states present in the matrix: 1 means that the state is present for the current species and 0 means not present. This input is a data matrix in tsv format without bit values and the output is a data matrix (matrix.tsv) containing a new column displaying these bit strings. 

The bit values are first written to be printed in table form, where at the end the cells in a row were sticked together to form a string. The reason was that initially the idea was to print a matrix for every character, containing all states and species.

ModifyNumerics.py
This code modifies all numerical values in a data matrix. Dimensions values are divided in length and with, and ranges in minimum and maximum. New columns are constructed only displaying the numerical values for a character. Some modules of the library pyuom are used fir the unit conversion.

CleanMatrix.py
This function removes the columns from the FlorML matrices which are not needed for the analysis. It also makes the names of the characters easier to interpret.



