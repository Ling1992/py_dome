# -*- coding: utf-8 -*-
__author__ = 'wly'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import requests

import re
import time
import Queue


import threading
from pyquery import PyQuery as pq



class SetQueue(Queue.Queue):
    def _init(self, maxsize):
        self.queue = set()
    def _put(self, item):
        self.queue.add(item)
    def _get(self):
        return self.queue.pop()


urlq = SetQueue()

def addw():
    while 1:
        api = 'http://www.vtalking.cn/index.php/api/remenapi'

        response = requests.get(api).json()
        if response:
            # print urlq.qsize()
            [urlq.put(url.replace('hxfhxf.com','xiezila.com')) for url in response if 'hxfhxf' in url]
        else:
            print 'empty..'
            time.sleep(660)


def getw():
    while 1:
        
        try:
            url = urlq.get_nowait()
            print 'get url'
            yield url
        except Exception as e:
            print 'now waiting...'
            time.sleep(10)

def work():
    for w in getw():
        data = fetch(w)
        if data:
            save(data)


def fetch(url):
    print url
    # url = 'http://www.hxfhxf.com/59913.html'
    headers = {
        "agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        jq = pq(response.text)
        data = {}
        data['url'] = response.url.replace('xiezila.com', 'hxfhxf.com')
        print "====get page====="
        if jq.find(".categories-links"):
            data['type'] = jq.find(".categories-links>a").text()
        if jq.find(".entry-date"):
            data['time'] = int(time.mktime(time.strptime(jq.find(".entry-date").text(), "%Y-%m-%d")))
        if jq.find(".entry-header>.entry-title"):
            data['title'] = jq.find(".entry-header>.entry-title").text()

        if jq.find(".entry-content"):
            data['desc'] = jq.find(".entry-content").html()
            group = re.findall(r'<img.+src="([^"]+).*>', data['desc'])
            if group:
                data['img'] = group[0]
        return data
    else:
        return False

def save(data):
        # print 'sdfsdfsdfsd'
        print data['title'].encode('gbk', 'ignore')
        data['url'] = data['url'].replace('xiezila.com', 'hxfhxf.com')
        for x in range(3):
            try:
                r = requests.post("http://www.vtalking.cn/index.php/api/moviesave", data = {"data": json.dumps(data)})
                print r.text
                print "save ok"
                return 
            except Exception, e:
                print Exception, e
                time.sleep(3)

def main():
    
    headers = {
        "agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }


if __name__ == "__main__":
    try:
        # addw()
        threads = []
        tget = threading.Thread(target=addw, name='geturl')
        threads.append(tget)
        gwork = threading.Thread(target=work, name='work')
        threads.append(gwork)
        for t in threads:
            t.start()

        for t in threads:
            t.join()
        
    except Exception as e:
        pass

