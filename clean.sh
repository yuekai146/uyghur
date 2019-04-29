RAW_TEXT=$1

SCRIPTS=/home/zhaoyuekai/uy/mosesdecoder/scripts
SPLITER=/home/zhaoyuekai/uy/mono/scripts/split.py
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
NORM_PUNC=$SCRIPTS/tokenizer/normalize-punctuation.perl
REM_NON_PRINT_CHAR=$SCRIPTS/tokenizer/remove-non-printing-char.perl
LATIN_CONVERTER=/home/zhaoyuekai/uy/uyghur-converter/test.py
DUP_FILTER=/home/zhaoyuekai/uy/uyghur-converter/clean.py

# Convert uyghur to latin characters
echo "Turn to latin chars."
python $LATIN_CONVERTER -s $RAW_TEXT -t $RAW_TEXT.latin

# Split paragraph into sentences
python $SPLITER -f $RAW_TEXT.latin -t $RAW_TEXT.latin.splited

# Filter duplicated paragraphs
mkdir tmp
n=1
while read line; do echo "$line" >> ./tmp/$n.txt; n=$((n+1)); done < $RAW_TEXT.latin.splited

echo "Remove duplicates"
python $DUP_FILTER -d "./tmp/"

# Make a non-duplicate file
cat ./clean_files.list | xargs cat >> $RAW_TEXT.latin.splited.clean
rm -rf ./tmp
