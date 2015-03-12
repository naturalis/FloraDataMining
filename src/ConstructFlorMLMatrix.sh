
python src/SplitColumns.py matrix_A27.tsv data/terms_and_categories.txt
echo "Columns splitted"
mv matrix.tsv input.tsv

python src/ConvertNominalsToBit.py input.tsv data/terms_and_categories.txt
echo "Nominals converted"
mv matrix.tsv input.tsv

python src/ClearNumerics.py input.tsv
