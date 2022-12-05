FOLDER=$(pwd)
GPUS=$1
MODE=$2
TRAIN=$3
TEST=$4
INDEX=$5

CUDA_VISIBLE_DEVICES=${GPUS} python3 code/faiss.py --mode ${MODE} \
 --file_dir ${FOLDER}/MSMT/ \
 --train ${TRAIN} --test ${TEST} --index_path ${INDEX}