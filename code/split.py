from tqdm import tqdm
import argparse


def parse_opt():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--file_path', type=str, default="", help="the location of file")
    parser.add_argument('--src_path', type=str, default="", help="the output location of src file")
    parser.add_argument('--trg_path', type=str, default="", help="the output location of trg file")
    
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_opt()
    file_path, src_path, trg_path = args["file_path"], args["src_path"], args["trg_path"]
    with open(file_path, "r") as f, open(src_path, "w") as fen, open(trg_path, "w") as fzh:
        for line in tqdm(f):
            dic = eval(line.strip(),{"false":False,"true":True})
            assert dic["src_lang"]=="zh"
            fzh.write(dic["src_text"]+"\n")
            fen.write(dic["trg_text"]+"\n")
