import jieba


if __name__ == '__main__':
    name = '穿越火线'
    f = open('c:/%s_输出.txt' % name, 'r')
    w = open('c:/结果/%s.txt' % name, 'w')
    s = ['的','了','么','呢','是','嘛','个','都','也','比','还','这','于','与','才','用','就','在','对','去','后','说','之']

    while True:
        line = f.readline()

        if not line:
            break
        flag = False
        if len(list(jieba.cut(line.split(' ')[0]))) > 1:
            for word in s:
                if line.split(' ')[0].startswith(word):
                    print(line)
                    flag = True
                    break
            if not flag :
                print('能分开...' + line)
                w.write(line)
        else:
            print('不能分...' + line)
            pass
    f.close()
    w.close()