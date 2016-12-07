import pickle
import tkinter
import tkinter.font as tkFont
import sys
from random import shuffle

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


def add(f):
    global count
    if f:
        pos.append(lists[count])
    else:
        neg.append(lists[count])
    count += 1

    if count >= len(comments):
        frame.quit()
        return

    text.delete(0.0, tkinter.END)

    if comments[count]:
        while comments[count][5] < 30:
            neg.append(lists[count])
            count += 1
        text.insert(0.0, comments[count][2])
        text.insert(tkinter.END, '\n\n')
        text.insert(tkinter.END, '%s星' % (comments[count][5] / 10))
    text.update()


def read():
    pos = pickle.load(open("pos_review.pkl", 'rb'))
    neg = pickle.load(open("neg_review.pkl", 'rb'))
    print(pos)
    print(neg)


if __name__ == '__main__':
    getStop()
    pos = pickle.load(open("pos_review.pkl", 'rb'))
    neg = pickle.load(open("neg_review.pkl", 'rb'))
    print(len(pos))
    print(len(neg))

    while [] in pos:
        pos.pop(pos.index([]))
    while [] in neg:
        neg.pop(neg.index([]))

    comments = list(DbUtil.getAllResult("select * from comment limit 10000 offset 20000"))

    shuffle(comments)
    comments = comments[:100]
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
    ft = tkFont.Font(family='黑体', size=20, weight=tkFont.BOLD)

    text = tkinter.Text(frame, font=ft, height=10, width=30)

    g = tkinter.Button(frame, text="好", width=12, command=lambda: add(True))
    b = tkinter.Button(frame, text="坏", width=12, command=lambda: add(False))
    text.pack()
    g.pack()
    b.pack()

    text.insert(0.0, comments[0][2])
    text.insert(tkinter.END, '\n\n')
    text.insert(tkinter.END, '%s星' % (comments[0][5] / 10))

    tkinter.mainloop()

    # pickle.dump(pos, file=open('pos_review.pkl', 'wb'))
    # pickle.dump(neg, file=open('neg_review.pkl', 'wb'))
