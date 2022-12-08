FOLDER=$(pwd)
RAW=$1
OUTPUT=$2

python3 code/detokenized.py --file_path ${FOLDER}/${RAW} \
 --output_path ${FOLDER}/${OUTPUT}
