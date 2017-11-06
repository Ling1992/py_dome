# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import requests
import json
import time
from pyquery import PyQuery as pq


def strtotime_wb(str):
    now = int(time.time())
    if str.find(u'小时前') != -1:
        print u'小时前'
        stamp = now - int(str[0:-3]) * 60 * 60
    elif str.find(u'分钟前') != -1:
        print u'分钟前'
        stamp = now - int(str[0:-3]) * 60
    elif str.find(u'刚刚') != -1:
        print u'刚刚'
        stamp = now
    elif str.find(u'昨天') != -1:
        print u'昨天'
        yestoday = time.localtime(now - 24*60*60)
        dt = time.strftime("%Y-%m-%d", yestoday)
        tail = str[2:]
        dt = dt + tail
        timearr = time.strptime(dt, "%Y-%m-%d %H:%M")
        stamp = int(time.mktime(timearr))
    elif len(str) == 10:
        print u'一年前'
        timearr = time.strptime(str, "%Y-%m-%d")
        stamp = int(time.mktime(timearr))
    elif len(str) == 5:
        print u'当年'
        today = time.localtime(now)
        dt = time.strftime("%Y-", today)
        dt = dt + str
        timearr = time.strptime(dt, "%Y-%m-%d")
        stamp = int(time.mktime(timearr))
    
    return stamp



class hotwb(object):

    uapi = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={0}&containerid=107603{1}&page={2}'
    saveapi = 'http://www.vtalking.cn/index.php/api/hotwbsave'
    uidapi = 'http://www.vtalking.cn/index.php/api/hotwbuser'

    hot = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/53.0.2785.116 Safari/537.36",
        "Host": "m.weibo.cn",
    }

    def __init__(self):

        super(hotwb, self).__init__()
        


    def getcard(self, uid, page = 1):

        url = self.uapi.format(uid, uid, page)

        res = requests.get(url, headers=self.headers)
        print res

        res = res.json()
        print url

        self.parse(res)


    def parse(self, r):

        cards = r['cards']

        keymap = {"reposts_count":"reposts_count", "comments_count":"comments_count","attitudes_count":"attitudes_count","text":"text","mid":"mid", 'created_at':'created_at'}

        # print cards

        cards = [c for c in cards if c.has_key('mblog') and c['mblog']['comments_count'] > self.hot]

        # print cards

        if cards:

            for card in cards:
                
                data = {keymap[k]:v for k, v in card['mblog'].items() if k in keymap.keys()}
                data['uid'] = card['mblog']['user']['id']
                data['screen_name'] = card['mblog']['user']['screen_name']
                data['stamp'] = strtotime_wb(data['created_at'])
                for i in xrange(3):
                    try:
                        print data
                        r = requests.post(self.saveapi, data={"data":json.dumps(data)})
                        print r.text
                        break

                    except Exception as e:
                        print e
                        time.sleep(10)


    def uiditer(self):

        while 1:
            try:
                uids = requests.get(self.uidapi).json()
                print uids

                if uids['status'] == 0:

                    for uid in uids['data']:
                        print uid
                        time.sleep(2)
                        yield uid
                else:
                    print 'waiting for task'
                    time.sleep(300)

            except Exception as e:
                time.sleep(60)

    def work(self):

        for uid in self.uiditer():
            print uid
            for x in xrange(1, 4):

                self.getcard(uid, x)
                time.sleep(2)

    def getwbuser(self):
        api = 'https://m.weibo.cn/api/container/getIndex?type=user&queryVal=电影&luicode=10000011&lfid=106003type%3D1&title=%E7%94%B5%E5%BD%B1&containerid=100103type%3D3%26q%3D%E7%94%B5%E5%BD%B1&page={0}'

        for x in xrange(2, 15):
            print api.format(x)
            res = requests.get(api.format(x), headers=self.headers)
            group = res.json()['cards'][0]['card_group']

            # uids =  [item['itemid'].split('=')[1].strip('&') for item in group]
            km = {'id': 'uid', 'profile_url': 'avatar', 'screen_name':'uname'}            

            users = [{km[k]:v for k, v in item.items() if k in km.keys()} for item in [item['user'] for item in group]]

            print users
            # print uids

            res = requests.post('http://www.vtalking.cn/index.php/api/wbusersave', data={'data':json.dumps(users)})

            print res.text
            time.sleep(3)

if __name__ == "__main__":
    h = hotwb()
    h.work()
    # h.getwbuser()
    