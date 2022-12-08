from tqdm import tqdm

if __name__ == '__main__':
    with open("wmt2021_en_zh.json", "r") as f, open("wmt2021_en_zh.en", "w") as fen, open("wmt2021_en_zh.zh", "w") as fzh:
        for line in tqdm(f):
            dic = eval(line.strip(),{"false":False,"true":True})
            assert dic["src_lang"]=="zh"
            fzh.write(dic["src_text"]+"\n")
            fen.write(dic["trg_text"]+"\n")
