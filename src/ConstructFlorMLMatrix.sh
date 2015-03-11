
python src/SplitColumns.py results/CharacterSplitting/condensed_matrix.tsv data/terms_and_categories.txt

mv matrix.tsv input.tsv
head input.tsv
python src/ConvertNominalsToBit.py input.tsv data/terms_and_categories.txt

mv matrix.tsv input.tsv

python src/ClearNumerics.py input.tsv
