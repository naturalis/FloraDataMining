#python src/OrderFlorML.py data/A26_final.xml
#mv ordened.xml results/A26_ordened.xml

#for flormlFile in $*
#do
#	echo $flormlFile

#	python ../../src/MakeCharacterList.py $flormlFile > "../character_lists/characters_$flormlFile"
#done

#for characterList in $*
#do

#	cat  $characterList | sort | uniq > "sorted_$characterList"
#done

for flormlFile in $*
do
	echo $flormlFile

	python ../../src/OrderCharacters.py $flormlFile "../character_lists/sorted_characters_$flormlFile" 

	mv matrix.tsv $flormlFile"_matrix.tsv"

#	cp matrix.tsv input.tsv

#	python ../../src/SplitColumns.py $flormlFile ../../data/terms_and_categories.txt

#	mv matrix.tsv newchars_$flormlFile
	
#	cp matrix.tsv input.tsv

#	python src/ConvertNominalsToBit.py $flormlFile data/terms_and_categories.txt
	
#	mv matrix.tsv "bit_$flormlFile"

#	mv matrix.tsv input.tsv

#	python src/ClearNumerics.py input.tsv

#	mv matrix.tsv "num_$flormlFile"

#	python src/CleanMatrix.py input.tsv

#	mv matrix.tsv "final_$flormlFile"

done
