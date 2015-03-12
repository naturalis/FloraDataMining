FloraDataMining
===============

What is the project about?

Plant species can be determined with the help of some books mentioned Floras. There are multiple types of plants and multiple types of Floras. When a botanist wants to determine a plant he must access the correct Flora. 

To make these Floras more accessible, these are digitalized in an XML format mentioned FlorML. The XML format is recogizable for humans and for machines. 

The reason the digitalisation is not only the accessibility. When digitalized, the Flora data will be put into table form. Then, some tests can be performed with this table to find correlation between species and their traits (mentioned characters). So, the text in the new XML file is converted to a table with species on one axis and relevant plant features (characters) on the other axis. This is performed with the programming language Python.

The different steps in constructing the matrix

Parsing the relevant characters (MakeCharacterList.py FlorML file )
First a list was made of all characters that are in a particular FlorML file. With the help of this list, it is possible to select the characters relevant for the study by hand. Because some names are used to define different character types, all characters are displayed together with their superiors, like “/grandparent/parent/child”. 

Ordering the text in the FlorML file (OrderFlorML.py FlorML file)
Before continuing the matrix construction, the text in the current XML file had to be ordered. Converting the text from a book to XML is very comprehensive, and because of this there were some  incorrectnesses in where some text parts were displayed in the XML file. This makes the construction of the matrix with a programming language too complex. Because of this, a code was written to put the texts displayed on the wrong place to the correct places.

The construction of the final matrix (OrderCharacters.py (structured) 1.FlorML file 2.character list
Finally a code was written to construct a matrix with species and characters. The input files are a FlorML file, and a csv file including the relevant the characters. The output is a tab-delimited file containing the final matrix. The rows represent the species and the columns represent the characters. In this table some characters contained not enough information. The corresponding columns were removed by hand. 

Splitting of the characters in more categories (SplitColumns.py  1.tsv file containing matrix 2.term list)
After this, many fields in the table still contained many text and it was still difficult to categorize them, which is necessary for the analysis. Because of this, a code was written to split some characters in more different child characters. So, the FlorML file did not contain these new characters, but they were determined by looking what the text in the matrix described.

Converting the nominal characters into bit strings (ConvertNamesToBit.py 1.tsv file containing matrix 2.term list)
The nominal characters were divided into bit strings, dsiplaying a 0 when a value is absent and a 1 when a value is present. 

Dividing the numerical values (ClearNumerics tsv file containing matrix)
Fornsome characters there were multiple numerical values possible in a range or in length and with for dimensions. There are displayed in multiple columns: length, width, minimum, maximum. 

