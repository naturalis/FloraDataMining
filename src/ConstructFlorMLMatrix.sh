#python src/OrderFlorML.py data/A22_final2.xml
#mv ordened.xml results/A22_ordened.xml

#python src/MakeCharacterList.py results/A22_ordened.xml > out.txt
#echo "Character list constructed"
#cat  out.txt | sort | uniq > character_list.txt

#python src/OrderCharacters.py results/A22_ordened.xml character_list.txt
#cat matrix.txt
#cp matrix.tsv input.tsv
python src/SplitColumns.py input.tsv data/terms_and_categories.txt
#cp matrix.tsv input.tsv

#python src/ConvertNominalsToBit.py input.tsv data/terms_and_categories.txt
#mv matrix.tsv input.tsv

#python src/ClearNumerics.py input.tsv
