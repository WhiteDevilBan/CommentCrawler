import os
import os.path

root = 'C:\结果'
fileNameList = []
if __name__ == '__main__':
    for filename in os.walk(root):
        fileNameList = filename[2]

    dict = {}

    for file in fileNameList:
        f = open(root+'\\'+file)
        while True:
            line = f.readline()
            if not line:
                break
            key = line.split(' ')[0]
            count = line.split(' ')[1]
            dict[key] = count


    for (k,v) in dict.items():
        print(k,v)
        f = open(root + '\\' + 'dict.txt', 'a')
        # f.write(dict)
        f.write((k+' '+v))
    f.close()