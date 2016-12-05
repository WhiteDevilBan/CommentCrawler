import pickle
import tkinter

import sys

from site.mybzz.util import DbUtil
import jieba

stop = []


def getStop():
    f = open("../StopWords.txt", encoding="utf-8")
    jieba.load_userdict("c:/dict.txt")

    while True:
        line = f.readline().replace("\n", '')

        if not line:
            break
        stop.append(line)


def add(index, f):
    global count
    count += 1
    text.delete(0.0, tkinter.END)
    if comments[index]:
        text.insert(0.0, comments[index][2])
    text.update()
    if f:
        pos.append(lists[index])
    else:
        neg.append(lists[index])
    if count > len(comments):
        sys.exit()


def read():
    pos = pickle.load(open("pos_review.pkl", 'rb'))
    neg = pickle.load(open("neg_review.pkl", 'rb'))
    print(pos)
    print(neg)


if __name__ == '__main__':
    pos = []
    neg = []

    # read()

    comments = DbUtil.getAllResult("select * from comment limit 30")
    lists = []
    for comment in comments:
        list = []
        result = jieba.cut(comment[2])
        for word in result:
            if word not in stop and word != ' ':
                list.append(word)

        lists.append(list)
    count = 0

    frame = tkinter.Tk()
    text = tkinter.Text(frame)
    g = tkinter.Button(frame, text="好", command=lambda: add(count, True))
    b = tkinter.Button(frame, text="坏", command=lambda: add(count, False))
    text.pack()
    g.pack()
    b.pack()
    tkinter.mainloop()

    pickle.dump(pos, file=open('pos_review.pkl', 'wb'))
    pickle.dump(neg, file=open('neg_review.pkl', 'wb'))
