import random

def getTime(date):
    return '2016-12-%s %s:%s:%s'%(date,random.randint(0,23),random.randint(0,59),random.randint(0,59))

if __name__ == '__main__':
    for i in range(1,3000):
        print('2016-12-%s %s:%s:%s'%(i,random.randint(0,23),random.randint(0,59),random.randint(0,59)))