python src/MakeCharacterList.py results/A27_ordened.xml > out.txt
echo "Character list constructed"
cat  out.txt | sort | uniq > character_list.txt

python src/OrderCharacters.py results/A27_ordened.xml character_list.txt
echo "Characters ordened to matrix"
mv matrix.tsv input.tsv

python src/SplitColumns.py input.tsv data/terms_and_categories.txt
echo "Columns splitted"
mv matrix.tsv input.tsv

python src/ConvertNominalsToBit.py input.tsv data/terms_and_categories.txt
echo "Nominals converted"
mv matrix.tsv input.tsv

python src/ClearNumerics.py input.tsv
