from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
import faiss # pip install faiss-gpu --no-cache
import numpy as np
import argparse

def parse_opt():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--mode', type=str, default="", choices=['train', 'test'], help="")
    parser.add_argument('--file_dir', type=str, default="", help="the location of file")
    parser.add_argument('--dataset', type=str, default="", help="the train/test set name")
    parser.add_argument('--index_path', type=str, default="trained_index", help="the test set name")
    
    args = parser.parse_args()

    return args


def batch_control(src_texts, batch=1024):
        res = [[]]
        for src_text in src_texts:
            if len(res[-1]) == batch:
                res.append([])
            res[-1].append(src_text)
        return res
    
    
def embed(text_path):
    use_gpu = True
    model_name_or_path = "xlm-roberta-base"
    device = torch.device("cuda:0") if use_gpu else torch.device("cpu")
    model = AutoModelForMaskedLM.from_pretrained(model_name_or_path, output_hidden_states=True).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

    with open(text_path, "r") as f:
        mono_texts = [line.strip() for line in f.readlines()]
    texts_embeddings = np.empty(shape=(0,768))
    for batch_texts in batch_control(mono_texts):
        with torch.no_grad():
            input_pt = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True).to(device)
            output_pt = model(**input_pt).hidden_states[0].cpu().numpy()
            batch_embeddings = output_pt.mean(axis=1)
        texts_embeddings = np.concatenate((texts_embeddings, batch_embeddings),axis=0)
    return texts_embeddings


if __name__ == '__main__':
    args = parse_opt()
    file_dir = args["file_dir"]
    
    if args["mode"] == "train":
        xb = embed(args["{file_dir}/dataset"]).astype("float32")
        print("hidden size:", xb.shape)

        # dim, measure = 768, faiss.METRIC_L2
        dim, measure = 768, faiss.METRIC_INNER_PRODUCT
        # param = 'Flat'
        param = 'IVF1024,PQ32'
        
        index = faiss.index_factory(dim, param, measure)
        gpu_index = faiss.index_cpu_to_all_gpu(index) # use all GPUs
        print(gpu_index.is_trained) # 输出为True

        gpu_index.add(xb) # 向index中添加向量
        cpu_index = faiss.index_gpu_to_cpu(gpu_index)
        faiss.write_index(cpu_index, "{file_dir}/trained.index")
    
    elif args["mode"] == "test":
        index = faiss.read_index(args["index_path"])
        xq = embed(args["{file_dir}/dataset"]).astype("float32")
        
        gpu_num = faiss.get_num_gpus()
        if use_gpu and gpu_num > 0:
            index = faiss.index_cpu_to_all_gpus(index)
        
        k = 10 # topK的K值
        D, I = gpu_index_flat.search(xq, k) # xq为待检索向量，返回的I为每个待检索query最相似TopK的索引list，D为其对应的距离
        print(I[:5])

        np.save("{file_dir}/I.npy", I)
        np.save("{file_dir}/D.npy", D)
