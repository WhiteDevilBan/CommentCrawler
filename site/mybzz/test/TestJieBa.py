import os

import jieba
import jieba.posseg as pseg

if __name__ == '__main__':

    result = jieba.cut("超爽的视觉盛宴，真实还原端游的质感，一万个赞")

    f = open("../StopWords.txt",encoding="utf-8")
    l = []
    while True:
        line = f.readline().replace("\n",'')
        # print(line)
        if not line:
            break
        l.append(line)
    # print(l)
    for seg in result:
        if seg not in l:
            print(seg)

