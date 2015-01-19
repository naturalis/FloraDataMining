FloraDataMining
===============

What is the project about?

Plants species can be determined with the help of  a books mentioned Flora's. These Flora's are digitalized in an XML format mentioned FlorML to make them more accessible. When digitalized, the Flora data can be mined when it is put in table form. Because of this, a matrix is developed with species on one axis and relevant plant features (characters) on the other axis. To do this, first the characters present in the FlorML file were listed and the text belonging to some relevant elements in the FlorML file was ordered more. All these steps are performed with the programming language Python.

Parsing the relevant characters
The python script MakeCharacterList.py makes a list of all characters in a FlorML file. The input is the FlorML file, and the output is the character list. Because some names are used for different character types, all characters are displayed together with their superiors on the axis of the matrix,  like for example “/grandparent/parent/child”. This list is used to build the matrix, and relevant characters can be selected from this list. 

Ordering the text in the FlorML file
The text belonging to some elements in the FlorML files first must be ordered, before the matrix could be constructed. There were some places where the text belonging to the relevant elements did not occur on the correct place. The script OrderXml.py reads a FlorML file, and gives as output,  FlorML file containing the same information with the text put at the correct places.

Constructing the final matrix
The python script OrderCharacters.py constructs a matrix of the species and the characters. The input files are a FlorML file, and a csv file including the relevant the characters, their number, “Y” or “N” to select which characters are relevant, and some notes on each line like: “1,/dispersal,N,1x mentioned”.  This will probably be changed to make the script read a list containing the relevant characters instead of this specific format, but until now this gave some unwanted newline characters in the matrix. The output is a tab-delimited file containing the final matrix. 

