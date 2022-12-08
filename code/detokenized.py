# -*- coding: utf-8 -*-
# create@ 2022-12-8 15:50

import json
from opencc import OpenCC
from sacremoses import MosesDetokenizer

if __name__ == '__main__':
    detokenizer = MosesDetokenizer('en')
    convert = OpenCC('t2s').convert

    for file in os.listdir("data"):
        with open('data/'+file, 'r') as fr, open('clean/'+file, 'w') as fw:
            for line in tqdm(fr):
                try:
                    dd = json.loads(line)
                except Exception:
                    continue
                src_lang, trg_lang = dd['src_lang'], dd['trg_lang']
                src_text, trg_text = dd['src_text'], dd['trg_text']
                if src_lang == 'en':
                    src_lang, trg_lang = trg_lang, src_lang
                    src_text, trg_text = trg_text, src_text
                if not (src_lang == 'zh' and trg_lang == 'en'):
                    continue
                src_text = convert(src_text)
                trg_text = detokenizer.detokenize([trg_text])
                dd['src_lang'], dd['trg_lang'] = src_lang, trg_lang
                dd['src_text'], dd['trg_text'] = src_text, trg_text
                dd['tokenized'] = False
                fw.write(json.dumps(dd, ensure_ascii=False)+'\n')
