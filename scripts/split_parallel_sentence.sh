FOLDER=$(pwd)
RAW=$1
SRC=$2
TRG=$3

python3 code/split.py --file_path ${FOLDER}/${RAW} \
 --src_path ${FOLDER}/${SRC} \
 --trg_path ${FOLDER}/${TRG}
