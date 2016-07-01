import random
from operator import itemgetter

from pytagcloud import make_tags, create_tag_image
from pytagcloud.colors import COLOR_SCHEMES

path= 'c:/结果/dict.txt'
if __name__ == '__main__':

    dict = {}

    f = open(path)
    while True:
        line = f.readline()

        if not line:
            break
        dict[line.split(' ')[0]] = int(line.split(' ')[1])


    swd = sorted(dict.items(), key=itemgetter(1), reverse=True)
    swd = swd[1:50]
    print(swd)

    dict ={}

    for (k,v) in swd:
        # print(k,v)
        dict[k] = v
    print(dict)
    # tags = make_tags(swd,
    #                  minsize=30,
    #                  maxsize=130,
    #                  colors=random.choice(list(COLOR_SCHEMES.values())))
    #
    # create_tag_image(tags,
    #                  'tag_cloud.png',
    #                  background=(0, 0, 0, 255),
    #                  size=(1280, 900),
    #                  fontname='SimHei')
    #
    # print('having save file to dick')