# -*- coding: utf-8 -*-
import time
import json
import threading
import Queue
import os
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("/Users/ling/PycharmProjects/py_dome/")


class LingSpider(object):

    threads = []

    def __init__(self, pid_file_name):
        (name, ext) = os.path.splitext(pid_file_name)
        self.pid_file_name = name
        self.pid_file_path = None
        self.project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.q = Queue.Queue(255)
        self.pq = Queue.Queue(22)

    # pid 文件处理
    def create_pid_file(self):
        self.pid_file_path = '{0}/cache/{1}.pid'.format(self.project_path, self.pid_file_name)
        with open('{0}/cache/{1}.pid'.format(self.project_path, self.pid_file_name), 'w') as f:
            f.write('{}'.format(os.getpid()))

    def del_pid_file(self):
        if self.pid_file_path is not None:
            os.remove(self.pid_file_path)
            pass

    def run(self):
        print u'run'
        self.create_pid_file()
        th = []

        for name in self.threads:
            tf = threading.Thread(target=LingSpider.__start, args=(self,), name=name)
            th.append(tf)

        t = threading.Thread(target=LingSpider.queue_work, args=(self,), name='queue')
        th.append(t)

        for t in th:
            t.start()
        for t in th:
            t.join()

        print 'game over'
        if os.path.isfile(self.pid_file_path):
            self.del_pid_file()

    def __start(self):
        self.init()
        while os.path.isfile(self.pid_file_path):
            res = self.spider()
            if res is False:
                break
        self.end()

    def init(self):
        pass

    def end(self):
        self.log(u'当前线程 结束！！！！')
        pass

    def spider(self):
        print 'spider'

    def queue_work(self):
        print u'queue_work'
        # del pid 强制结束
        index = 1
        while os.path.isfile(self.pid_file_path) and threading.active_count() > 2:
            print u"当前线程数：", threading.active_count()
            self.log(u"当前线程数: {}".format(threading.active_count()))
            if self.q.qsize() >= 1:
                self.log(u"get queue start")
                item = self.q.get_nowait()
                self.log(u"get queue over")
                res = self.save(item)
                print u"save response:", res
                index = 1
            else:
                index += 1
                print u'no item sleep 3s'
                self.log(u'queue sleep 3s ')
                self.log(u"当前线程数: {}".format(threading.active_count()))
                time.sleep(3)
                if index >= 20:
                    self.del_pid_file()
        print u"当前线程数：", threading.active_count()
        print 'queue is over'
        self.log(u"当前线程数: {}".format(threading.active_count()))
        self.log(u'queue 队列结束 ！！！！')

    def save(self, item):
        print u'save'
        print u"save --> item:", item
        return {}

    # 日志 记录
    def log(self, content, key_str='default'):
        name = threading.current_thread().name
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        log_path = "{}/cache/{}".format(self.project_path, self.pid_file_name)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        with open("{}/{}_{}.log".format(log_path, time.strftime("%Y-%m-%d", time.localtime(time.time())), name), 'a') as f:
            f.write('{} -->>'.format(key_str))
            f.write('{}:\n'.format(now))
            f.write('\t')
            f.write(json.dumps(content, ensure_ascii=False, encoding='utf-8'))
            f.write('\n')

    def get_json_obj(self, string_1):
        print 'start'
        reg1 = re.compile(r'{((?!}).)*')
        reg2 = re.compile(r'}((?!{).)*')
        reg3 = re.compile(r'{')
        reg4 = re.compile(r'}')
        string_1 = re.sub(r'[^{}]*', '', string_1, 1)
        index1 = 0
        index2 = 0
        res = ''
        while index1 != index2 or index1 == 0:
            s = reg1.search(string_1)
            if s:
                res = res + s.group()
                index1 = len(reg3.findall(s.group())) + index1
                string_1 = reg1.sub("", string_1, 1)
            else:
                pass
            s = reg2.search(string_1)
            if s:
                res = res + s.group()
                index2 = len(reg4.findall(s.group())) + index2
                string_1 = reg2.sub("", string_1, 1)
            else:
                pass
        s = re.search(r'{[\s\S]*}', res)
        if s:
            res = s.group()
            res = json.loads(res)
        else:
            res = ''
        return res

    def __del__(self):
        if os.path.isfile(self.pid_file_path):
            self.del_pid_file()
        print '__del__ --> LingSpider'

    pass
