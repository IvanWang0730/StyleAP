# Controlling Style in Neural Machine Translation via Prompt-based Zero-shot Learning
Code and Data for Paper [Controlling Style in Neural Machine Translation via Prompt-based Zero-shot Learning](https://translate.volcengine.com/), this paper proposes 1) a dataset **m**ultiway **s**tylized **m**achine **t**ranslation (**MSMT**) benchmark, including four language directions with diverse language styles. 2) a **p**rompt-based **z**ero-shot **l**earning (**PZL**) method to avoid re-tuning time after time. Through automatic evaluation and human evaluation, our method achieves a re-markable improvement over baselines and other methods. A series of analysis also show the advantages of our method.

<p align="center">
<img src="method.pdf" width="350">
</p>

## Requirements:
- [neurst](https://github.com/bytedance/neurst)
- [huggingface transformer 4.25.1](https://github.com/huggingface/transformers)
- [torch 1.13.0](https://pytorch.org/)
- faiss-gpu 1.7.2

## Quick Start
### Datasets
Our experiments are implemented on MSMT with four language directions, i.e., en-zh, zh-en, en-ko, and en-pt. You can download the raw dataset used in our paper on [Google Drive](https://drive.google.com/drive/folders/17N2o0nc5i6aDNsHOQAoAbqbtVuPeaR4i?usp=share_link). It includes training, evaluation and innovated test sets as is depicted in our paper.
