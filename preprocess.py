from g2pc import G2pC
import re

from m_text_normalizer import TextNormalizer

def has_non_english_chars(text):
    return bool(re.search(r'[^A-Za-z]', text))
def proprecess(text, g2p):

    pinyin = ''
    pinyin_result = g2p(text)
    for pys in pinyin_result:
        for py in pys[3].split(' '):
            if py[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                # 去掉所有特殊符号
                if has_non_english_chars(py[:-1][-1]):
                    continue
                else:
                    pinyin += py[:-1] + ' '
            else:
                # 去掉所有特殊符号
                if has_non_english_chars(py):
                    continue
                else:
                    pinyin += py + ' '

    return pinyin

import time
import glob
import os
import shutil
from tqdm import tqdm  
if __name__ == "__main__":
    g2p = G2pC()
    text_normalizer = TextNormalizer()
    text_normalizer.load()

    texts = glob.glob("/datajuiceFS/a100/zulin/code/Montreal-Forced-Aligner_lastest/zz_test/wav/**/*.lab", recursive=True)


    
    for text_path in tqdm(texts):
        text = open(text_path, 'r').readline().strip()

        text = text_normalizer.normalize(text)
        pinyin = proprecess(text, g2p).strip() + '\n'

        # # 移动文件
        shutil.move(text_path, text_path.replace('.lab', '.txt'))
        open(text_path, 'w').write(pinyin)



