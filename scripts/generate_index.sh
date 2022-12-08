FOLDER=$(pwd)
GPUS=$1
DATASET=$2
INDEX=$3

CUDA_VISIBLE_DEVICES=${GPUS} python3 code/faiss.py --mode train \
 --file_dir ${FOLDER}/MSMT/ \
 --dataset ${DATASET} --index_path ${INDEX}
