# Controlling Style in Neural Machine Translation via Prompt-based Zero-shot Learning
Code and Data for Paper [Controlling Style in Neural Machine Translation via Prompt-based Zero-shot Learning](https://translate.volcengine.com/), this paper proposes 1) a dataset **m**ultiway **s**tylized **m**achine **t**ranslation (**MSMT**) benchmark, including four language directions with diverse language styles. 2) a **p**rompt-based **z**ero-shot **l**earning (**PZL**) method to avoid re-tuning time after time. Through automatic evaluation and human evaluation, our method achieves a re-markable improvement over baselines and other methods. A series of analysis also show the advantages of our method.

<p align="center">
<img src="method.pdf" width="350">
</p>

## Requirements
- [neurst](https://github.com/bytedance/neurst)
- [sacremoses](https://github.com/alvations/sacremoses)
- [subword-nmt](https://github.com/rsennrich/subword-nmt)
- [huggingface transformer 4.25.1](https://github.com/huggingface/transformers)
- [torch 1.13.0](https://pytorch.org/)
- faiss-gpu 1.7.2

**NOTE**: At the very beginning, install NeurST from source:
```
git clone https://github.com/IvanWang0730/PZL.git
cd neurst/
pip3 install -e .
```
If there exists ImportError during running, manually install the required packages at that time.

## Quick Start
### Datasets
Our experiments are implemented on MSMT with four language directions, i.e., en-zh, zh-en, en-ko, and en-pt. You can download the raw dataset used in our paper on [Google Drive](https://drive.google.com/drive/folders/17N2o0nc5i6aDNsHOQAoAbqbtVuPeaR4i?usp=share_link). It includes training, evaluation and innovated test sets as is depicted in our paper.

#### Multi-way Stylized Machine Translation(MSMT) Benchmark
|                        | en-zh              | zh-en              | en-ko                | en-pt               |
|------------------------|--------------------|--------------------|----------------------|---------------------|
| Styles                 | Modern / Classical | Modern / Early     | Honorific / Non-hono | Eurpean / Brazilian |
| Monolingual            |  22M /     967K    |  22M /   83.2K     |  20.5K /     20.5K   |  168K /    234K     |
| Parallel               |        9.12M       |        9.12M       |        271K          |        412K         |
| Development            |        1,997       |        2,000       |        879           |        890          | 
| Test                   |        1,200       |        1,182       |        1,191         |        857          |
- **Classical and Modern**. Classical Chinese originated from thousands of years ago and was used in ancient China. Modern Chinese is the normal Chinese that is commonly used currently.
- **Early Modern and Modern**. Early Modern English in this paper refers to English used in the Renaissance such as Shakespearean plays. Modern English is the normal English that is commonly used currently.
- **Honorific and Non-honorific**. There are seven verb paradigms or levels of verbs in Korean, each with its own unique set of verb endings used to denote the formality of a situation. We simplify the classification and roughly divide them into two groups.
- **European and Brazilian**. European Portuguese is mostly used in Portugal. Brazilian Portuguese is mostly used in Brazil.

### Create Prompt-based Data
We take en2zh task as an example to show how it works.
```shell
# generate faiss index
bash scripts/generate_index.sh 0 wmt2021_en_zh.en trained_en_zh.index
# search nearest samples via index
bash scripts/search_index.sh 0 wmt2021_en_zh.en trained_en_zh.index 
```
In this instance, we use `wmt2021_en_zh.en` in the default file directory `./MSMT/` to train a faiss index on a single GPU 0 and the same file to search the nearest monolingual sentences via the above trained index. **note**: You may use the `scripts/split_parallel_sentence.sh` to obtain monolingual sentence files.

You can quickly prepossess the training data like this. You can check [sacremoses](https://github.com/alvations/sacremoses) and [subword-nmt](https://github.com/rsennrich/subword-nmt) for other setting details.
```shell
sacremoses -l {src_lang} -j 4 tokenize  < {src_text} > {src_text}.tok
sacremoses -l {trg_lang} -j 4 tokenize  < {trg_text} > {trg_text}.tok
subword-nmt learn-joint-bpe-and-vocab --input {train_file}.L1 {train_file}.L2 -s {num_operations} -o {codes_file} --write-vocabulary {vocab_file}.L1 {vocab_file}.L2
```

### Training & Validating
We can directly use the yaml-style configuration files to train and evaluate a transformer model on [neurst](https://github.com/bytedance/neurst).
```shell
python3 -m neurst.cli.run_exp \
    --config_paths configs/training_args.yml,configs/translation_bpe.yml,configs/validation_args.yml \
    --hparams_set transformer_base \
    --model_dir /models/benchmark_base
```
where /models/benchmark_base is the root path for checkpoints. Here we use --hparams_set transformer_base to train a transformer model including 6 encoder layers and 6 decoder layers with dmodel=512.

### Evaluation on Testset
By running with
```shell
python3 -m neurst.cli.run_exp \
    --config_paths configs/prediction_args.yml \
    --model_dir configs/benchmark_base/best_avg
```
BLEU scores will be reported on MSMT testset.

## Citation

```
@article{2022-PZL,
    title = "Controlling Style in Neural Machine Translation via Prompt-based Zero-shot Learning",
    author = "",
    year = "2022",
    journal = "arXiv",
}
```

Please kindly cite our paper if this paper and the codes are helpful.

## Thanks

Many thanks to the GitHub repositories of [Transformers](https://github.com/huggingface/transformers), [Neurst](https://github.com/bytedance/neurst) and [Lightseq](https://github.com/bytedance/lightseq). Part of our codes are modified based on their codes.
