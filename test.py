# _*_ encoding=utf-8 _*_
import threading
from time import ctime, sleep


def loop(loops, sec, arg):
    print 'sec:', sec
    print 'loops : ', loops, 'sec:', ctime(), 'arg:', repr(arg)
    sleep(sec)
    print 'loops : ', loops, 'sec:', ctime(), 'current thread name:', threading.current_thread().name
    test(arg)


def test(arg):
    print __name__, arg
    print 'current thread name:', threading.current_thread().name

if __name__ == '__main__':
    category = {'new': {'name': 'news1', 'index': 2}, 'sport': {'name': 'sport1', 'index': 8}}

    threads = []

    for key in category:
        print key, category[key]['index'], category[key]['name']
        t = threading.Thread(target=loop, args=(key, category[key]['index'], category[key]['name']), name='{}121'.format(key))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

