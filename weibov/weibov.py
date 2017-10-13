# -*- coding: utf-8 -*-
import requests
import cookielib
import json
import time
import threading
import sys
import traceback

import base64
import binascii

import urllib
import rsa
import re
import random
import logging

import urlparse

import Queue

from pyquery import PyQuery as pq



reload(sys)
sys.setdefaultencoding("utf-8")


def wbreson(url):
    str = urlparse.parse_qs(url)['reason'][0]
    str = unicode(eval(repr(str)), 'gbk')
    print str


def wbcode(s):
    s = unicode(eval(repr(s)), 'gbk')
    return s

class manager(object):

    wk_get = 'http://www.vtalking.cn/57adm.php/weiboapi/cmtapi?appid='
    wk_pt = 'http://www.vtalking.cn/57adm.php/weiboapi/cmtapi_add?appid='
    appid = 'olK3L008IooQmmrZwxO1PFBJfIb0'

    sayHello = [u'@电影收录君 来一个', u'你们居然不知道@电影爬虫君 那里可以看', u'@电影爬虫君 正在免费fen想，速去围观吧', u'这个电影我早在@电影爬虫君 那里看过了',  u'好哒', u'@电影爬虫君 那里就可以mian费观看啊', u'傻孩子，去@电影爬虫君 那里可以看的', u'科普一下：@电影爬虫君 会免费给你找汁源哒', u'还没看过的快去@电影爬虫君 吧', u'@电影爬虫君 可以看哦，亲测， 记得回来点个赞哦',u'大赞啊,在@电影图剪 那里找到了',u'我在@电影收录君 那里找到啦，棒棒哒',u'你们居然不知道@电影收录君 那里可以看',u'你也是棒，在@电影图剪 那里就有啊', u'找不到资源，谁能告诉我怎么找[二哈]']

    def __init__(self):

        super(manager, self).__init__()

    @classmethod
    def getwk(cls):
        return requests.get(cls.wk_get + cls.appid).json()

    @classmethod
    def putwk(cls, data):
        return requests.post(cls.wk_pt + cls.appid, data={'str': json.dumps(data)})
    @classmethod
    def getmsg(cls, self):
        while 1:
            tmp = cls.sayHello.pop()
            cls.sayHello.insert(0, tmp)
            yield tmp




class weibo(object):
    appid = 'olK3L0_jTSwjmHj-okGxImTsFP0w'
    prelogin_url = "https://login.sina.com.cn/sso/prelogin.php"
    loginapi = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    client = "ssologin.js(v1.4.18)"

    time_diff = (600, 900)


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/53.0.2785.116 Safari/537.36",
        "Host": "login.sina.com.cn",
    }

    count = 0



    def __init__(self, name, ini, queque):
        super(weibo, self).__init__()
        self.workq = queque
        self.ns = name
        self.ini = ini

        self.su = base64.b64encode(urllib.quote(self.ini['username']))

        self.rq = self._getrq()


    def _getrq(self):

        session = requests.Session()

        print "{0}-{1}".format(self.ns, threading.currentThread().getName())
        session.cookies = cookielib.LWPCookieJar(filename="{0}-{1}.txt".format(self.ns, threading.currentThread().getName()))

        try:
            session.cookies.load(ignore_discard = True)

        except:
            print u'load cookies faild'

        return session



    def prelogin(self):

        payload = {"entry": "weibo", "callback": "sinaSSOController.preloginCallBack", "su": self.su, "rsakt": "mod","checkpin": 1, "client": self.client}
    
        res = self.rq.get(self.prelogin_url, params=payload, verify=False, headers=self.headers)

        self.rq.cookies.save()

        return res.text[35:-1]

    def _login(self, predata):

        predata = json.loads(predata)


        print 'prelogindata===', predata

        s = str(predata["servertime"]) + '\t' + str(predata["nonce"]) + '\n' + self.ini['pwd']

        key = rsa.PublicKey(int(predata["pubkey"], 16), int("10001", 16))

        key = rsa.encrypt(s, key)

        sp = binascii.b2a_hex(key)

        post_data = {"entry": "weibo",
            "gateway": 1,
            "from": "",
            "savestate": 7,
            "useticket": 1,
            "pagerefer": "",
            "pcid": predata["pcid"],
            "vsnf": 1,
            "su": self.su,
            "service": "miniblog",
            "servertime": int(time.time()),
            "nonce": predata["nonce"],
            "pwencode": "rsa2",
            "rsakv": predata["rsakv"],
            "sp": sp,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "prelt": "129",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META"
        }

        if predata.get('showpin', None) == 1:
            

            captcha = "http://login.sina.com.cn/cgi/pin.php?r={}&s=0&p={}".format("".join(random.sample("123456789", 8)),predata["pcid"])
            print u'验证码',  captcha, "\n"

            res = self.rq.get(captcha, headers=self.headers)

            print u'验证码响应', res
            with open("{0}_captcha.jpg".format(self.ini['username']), 'wb') as f:
                f.write(res.content)
                f.close()

            from PIL import Image
            try:
                im = Image.open("{0}_captcha.jpg".format(self.ini['username']))
                im.show()
                im.close()
            except Exception as e:
                print e
                pass
            captcha = raw_input('input:')
            post_data['door'] = captcha


        res = self.rq.post(self.loginapi, data=post_data, headers=self.headers)
        # print res.content
        if re.search("refresh", res.text):
            print res.url
            print u"验证码输入错误，重新登录中" 
            time.sleep(120)
            self.login()
        print res

        self.rq.cookies.save()

        url = re.findall("location.replace\('(.*?)'\)", res.text)

        if not url:
            url = re.findall("location.replace\(\"(.*?)\"\)", res.text)

        url = url[0]
        print 'url from login reuturn', url

        # 解析登录跳转的url
        param = urlparse.parse_qs(url)


        print 'loging-url===', res, res.url
                # 验证登陆，此处302跳转
        self.headers["Host"] = "passport.weibo.com"
        res = self.rq.get(url, allow_redirects=False, headers=self.headers)

        print res

        # 获得跳转链接
        location = res.headers["Location"]
        self.headers["Host"] = "weibo.com"
        print '302 redirect===', location

        res = self.rq.get(location, headers=self.headers)

        print res,res.url, res.text
        user_info = re.findall("parent.sinaSSOController.feedBackUrlCallBack\((.*?)\)", res.text)[0]
        user_info = json.loads(user_info)
        if user_info["result"]:
            print user_info

            print u'登录成功'
            self.rq.cookies.save()
            self.ini['userdomain'] = user_info["userinfo"]["userdomain"]
            self.ini['uniqueid'] = user_info["userinfo"]["uniqueid"]
        else:
            print u'登录失败'
            time.sleep(120)
            self.login()


       
    def autologin(self):

        res = self.rq.get('https://weibo.com/?category=99991')

        print res, res.content

        print 'firt-redirctto-----', res.url

        url = re.findall("location.replace\(\"(.*?)\"\)", res.text)

        if not url:

            self.login()
            return;
        url = url[0]

        print 'js-redirect----', url

        self.headers["Host"] = "passport.weibo.com"

        res = self.rq.get(url, allow_redirects=False, headers=self.headers)

        print res
      

        url = re.findall("location.replace\('(.*?)'\)", res.text)[0]
        print 'js-redirect2--', url

        self.headers["Host"] = "passport.weibo.com"
        res = self.rq.get(url, allow_redirects=False, headers=self.headers)

        print res
        # print res.headers

        location = res.headers["Location"]
        print '302 location---', location
        self.headers["Host"] = "weibo.com"
        res = self.rq.get(location, headers=self.headers)

        print res
        # if res.url.index('/u/'):
        #     uid = re.findall(r"\$CONFIG\['uid'\]=\'(\d+)\'", res.text)
        #     self.ini['uniqueid'] = uid[0]
        #     print uid
        #     print u'重新登录成功'
        # else:
        #     print u'重新登录失败'
        #     time.sleep(10)
        #     self.login()
        try:
            res.url.index('/u/')
            uid = re.findall(r"\$CONFIG\['uid'\]=\'(\d+)\'", res.text)
            self.ini['uniqueid'] = uid[0]
            print uid
            print u'登录成功，主页'
        except ValueError as e:

            try:
                res.url.index('/nguide/interest')

                grp = re.findall(r'\$CONFIG\s=\s({.+})', res.text, re.M | re.S)

                a = grp[0]

                config = eval(a)
                self.ini['uniqueid'] = config['uid']
                print u'登录成功，兴趣页'
            except Exception as e:

                print u'重新登录失败'
                time.sleep(10)
                self.login()
                pass


    def login(self):

        data = self.prelogin()
        self._login(data)

    def act(self, do, data):
        import datetime
        now = datetime.datetime.now()
        ftime = now.strftime("%Y-%m-%d %H:%M:%S")
        print u'操作时间{0}'.format(ftime)
        f = getattr(self, do)
        return f(data).json()



    def comment(self, ini):
        print u'第{0}次评论， 评论内容:{1},评论人:{2}, 微博id:{3}'.format(self.count, ini['content'], self.ini['nickname'], ini['mid']) 
       
        self.count = self.count + 1
        forward_data = {
            "act":"post",
            "mid":ini['mid'],
            "uid":self.ini['uniqueid'],
            "forward":"0",
            "isroot":"0",
            "content":ini['content'],
            "location":'v6_content_home',
            "module":"scommlist",
            "group_source":"",
            "tranandcomm":"1",
            "filter_actionlog":"",
            "pdetail":'',
            "_t":"0",
        }

        forwardapi = 'https://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd={0}'.format(int(time.time()))
                                                                
        self.headers["Origin"] = "http://weibo.com"
        self.headers["Referer"] = 'http://weibo.com/u/2476481021?refer_flag=1005055013_'

        res = self.rq.post(forwardapi, data=forward_data, headers=self.headers)
        print res
        try:
            r_comment = res.json()
        except Exception as e:
            print e
            pass

        if r_comment['code'] == '100000':
            print '----in----'
            hook_data = self.comment_hook(r_comment['data']['comment'])
            hook_data['mid'] = ini['mid']
            hook_data['cmt_id'] = ini['cmt_id']

            p_data = {'act': 'chalou', 'p': hook_data, 'worker': 'all', 'msgto': ini['content']}

            print manager.putwk(p_data).content

            
        else:
            try:
                print r_comment['msg']
            except Exception as e:
                print e
                pass

        return res

    def zan(self, ini):

        print u'第{0}次评论， 评论内容:{1},评论人:{2}, 微博id:{3}'.format(self.count, ini['content'], self.ini['nickname'], ini['mid']) 

        zanapi = 'http://weibo.com/aj/v6/like/add?ajwvr=6&__rnd={0}'.format(int(time.time()))

        like_data = {
            "location": "v6_content_home",
            'location':'page_100505_home',
            'version':'mini',
            'qid':'heart',
            'mid':ini['mid'],
            'loc':'profile',
            'cuslike':1,
            '_t':0
        }

        self.headers["Origin"] = "http://weibo.com"
        self.headers["Referer"] = 'http://weibo.com/u/2476481021?refer_flag=1005055013_'
        
        res = self.rq.post(zanapi, data=like_data, headers=self.headers)
        print res, res.json()

    def chalou(self, ini):

        print u'第{0}次评论， 评论内容:{1},评论人:{2}, 楼主：{3}, 微博id:{4}'.format(self.count, ini['content'], self.ini['nickname'], ini['nick'], ini['mid']) 

        chalouapi = 'https://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd={0}'.format(int(time.time()))

        self.count = self.count + 1

        chalou_data = {
            "act":"reply",
            "mid":ini['mid'],
            "cid":ini['cid'],
            "uid": self.ini['uniqueid'],
            "forward":"0",
            "isroot":"0",
            "content":ini['content'],
            "ouid":ini['ouid'],
            "nick":ini['nick'],
            "ispower":"1",
            "status_owner_user":"",
            "area":"2",
            "canUploadImage":"0",
            "module":"scommlist",
            # "dissDataFromFeed":"[object Object]",
            "approvalComment":"false",
            "root_comment_id":ini['cid'],
            "location":"page_100505_home",
            "pdetail":"''",
            "_t":"0",
        }

        self.headers["Origin"] = "http://weibo.com"
        self.headers["Referer"] = 'http://weibo.com/u/2476481021?refer_flag=1005055013_'

        res = self.rq.post(chalouapi, data=chalou_data, headers=self.headers)
        print res
        try:
            print res.json()['msg']
        except Exception as e:
            print e
            pass


        return res


    def comment_hook(self, html):
        # cid re.search(r'comment_id="(\d+)"', html).group(1)
        cid = re.search(r'cid=(\d+)', html).group(1)
        rid = re.search(r'rid=(\d+)', html).group(1)
        oid = re.search(r'oid=(\d+)', html)
        if oid:
            oid = oid.group(1)
        else:
            oid = self.ini['uniqueid']

        nick = pq(html).find(".W_fl img").attr('alt')

        return {'cid': cid, 'rid': rid, 'ouid': oid, 'nick': nick}

#     def nextwork(self):
#         try:
#             print 'qsize====',self.workq.qsize()
           
#             f, p, ns, content = self.workq.get_nowait()
#             p['content'] = content
#             print u'插楼内容:', p, self.ini['nickname']
            
#             time.sleep(random.randint(600, 660))
#             print u'休， 休息一下'
#             f = getattr(self, f)
# # https://m.weibo.cn/3644441127/4152136986103901
#             f(p)

#         except Exception as e:
#             print e

#             # print 'the queue is empty...'https://m.weibo.cn/2712860252/4152003191987010
#             time.sleep(10)
#             if self.ns == 'lw100847@163.com':
#                 self.act('comment', {'mid':'4152136986103901', 'content': self.getmsg().next()})

        

    def work(self):

        self.autologin()
        time.sleep(random.randint(5, 10))

        while 1:

            _imsg = manager.getwk()

            print _imsg

            if _imsg['status'] == 0:
                _imsg = json.loads(_imsg['data'])
                if _imsg['worker'] == self.ns or _imsg['worker'] == 'all':
                    self.act(_imsg['act'], _imsg['p'])
                    b, e = self.time_diff
                    time.sleep(random.randint(b, e))

            else:
                time.sleep(60)


    def pushweibo(self):
        api = 'http://weibo.com/p/aj/v6/mblog/add?ajwvr=6&domain=100505&__rnd={0}'.format(int(time.time()))

        post_data = {

            "content":"",
            "location":"page_100505_home",
            "text":"#我的第一条微博# 早安哈哈中，亲们[二哈]",
            "appkey":"",
            "style_type":"1",
            "pic_id":"",
            "tid":"",
            "pdetail":"",
            "rank":"0",
            "rankid":"",
            "pub_source":"page_2",
            "longtext":"1",
            "topic_id":"",
            "pub_type":"dialog",
            "_t":"0",
        }

        self.headers["Origin"] = "http://weibo.com"
        self.headers["Referer"] = 'http://weibo.com/u/{0}?refer_flag=1005055013_'.format(self.ini['uniqueid'])
 
        res = self.rq.post(api, data=post_data, headers=self.headers)
        print res.content

    def test(self):
        for i in xrange(5):

            print i
            print self.sayHello[i]


if __name__ == "__main__":

    if len(sys.argv) > 1:
        idx = int(sys.argv[1])
    else:
        idx = 0

    users = [

        {'username': '17135852484', 'pwd': 'na13022', 'nickname': u'橡皮擦8575'},
        {'username': '17135852348', 'pwd': 'na13022', 'nickname': u'豪情万千 pattern_74281'},
        # {'username': '17153983154', 'pwd': 'zm16010', 'nickname': u'电影大收录'},
        {'username': '17099104329', 'pwd': 'zm16010', 'nickname': u'电影小妹嚒'},
    ]

    workq = Queue.Queue()

    wb = weibo(users[idx]['username'], users[idx], workq)

    wb.work()
    # wb.autologin()
