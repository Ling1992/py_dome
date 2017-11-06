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

    wk_get = 'http://www.vtalking.cn/57adm.php/wbapibeta/cmtapi?appid='
    wk_pt = 'http://www.vtalking.cn/57adm.php/wbapibeta/cmtapi_add?appid='
    wb_task = 'http://www.vtalking.cn/57adm.php/wbapibeta/wbtaskget?appid='
    appid = 'olK3L0_jTSwjmHj-okGxImTsFP0w'

    u = [u'@电影图剪', u'@电影爬虫君', u'@电影追击令', u'@电影收录君']

    sayHello = [u'{0}{1} 那里dou有啊', u'{0}{1}你们居然不知道{1} 那里可以看', u'{0}{1} 正在fen想，速去围观吧', u'{0}这个我早在{1} 那里看过了',  u'{0}戳{1} ', u'{0}{1} 那里就可以mian费观看啊', u'{0}傻孩子，去{1} 那里可以看的', u'{0}科普一下：{1} 会给你找汁源哒', u'{0}还没看过的快去{1} 吧', u'{0}{1} 有哦，亲测， 记得回来点个zan哦',u'{0}大赞啊,在{1} 那里找到了',u'{0}我在{1} 那里找到啦，棒棒哒',u'{0}哈哈哈，我在{1} 那里看啦',u'{0}你们也是棒，在{1} 那里就有啊', u'{0}以前我也找不到，至从有了{1} ，再也没愁过啦[二哈]']

    def __init__(self):

        super(manager, self).__init__()


    @classmethod
    def h_wb_task(cls, data):
        if data['status'] is not 0:
            print data['data'];
            return data
        data = data['data']
        
        content = cls.getmsg().next()

        if data['cmtkw']:

            content = content.format(data['cmtkw'], cls.u[random.randint(0, len(cls.u) - 1)])

        else:
            content = content.format('', cls.u[random.randint(0, len(cls.u) - 1)])

        p = {'mid': data['wid'], 'content': content}

        data = {'status': 0, 'data': json.dumps({'act': 'comment', 'p': p, 'worker': 'all'})}
        return data

    @classmethod 
    def getwk(cls, t):
        hook = 'h_{0}'.format(t)
        try:
            r = requests.get(getattr(cls, t) + cls.appid)
            if r.status_code == 200:
                if getattr(cls, hook, None):
                    return getattr(cls, hook)(r.json())
                else:
                    return r.json()
            else:
                time.sleep(60)
                cls.getwk(t)


        except Exception as e:
            print e
            time.sleep(60)
            cls.getwk(t)



    @classmethod
    def putwk(cls, data):
        return requests.post(cls.wk_pt + cls.appid, data={'str': json.dumps(data)})

    @classmethod
    def getmsg(cls):
        while 1:
            tmp = cls.sayHello.pop()
            cls.sayHello.insert(0, tmp)
            yield tmp




class weibo(object):
    #17
    ua = USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    ]

    appid = 'olK3L0_jTSwjmHj-okGxImTsFP0w'
    prelogin_url = "https://login.sina.com.cn/sso/prelogin.php"
    loginapi = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    client = "ssologin.js(v1.4.18)"
    mod = 'online'

    time_diff = (480, 600)


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
        self.headers['User-Agent'] = self.ua[self.ini['ua']]

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
        try:
            uid = re.findall(r"\$CONFIG\['uid'\]=\'(\d+)\'", res.text)
            self.ini['uniqueid'] = uid[0]
            print uid
            print u'登录成功，主页'
        except Exception as e:
            print e
            try:
                grp = re.findall(r'\$CONFIG\s=\s({.+})', res.text, re.M|re.S)
           
                a =  grp[0]

                config = eval(a)
                self.ini['uniqueid'] = config['uid']
                print u'登录成功，' + res.url

            except Exception as e:
                print u'重新登录失败'
                time.sleep(10)
                self.login()


    def login(self):

        data = self.prelogin()
        print data
        self._login(data)

    def act(self, do, data):
        import datetime
        now = datetime.datetime.now()
        ftime = now.strftime("%Y-%m-%d %H:%M:%S")
        print u'操作时间{0}'.format(ftime)
        f = getattr(self, do)
        return f(data)



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
        if res.status_code == 200:
            r_comment = res.json()
        
            if self.mod == 'online' and r_comment and r_comment['code'] == '100000':

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

        else:
            print res.content

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
        self.headers["Referer"] = 'http://weibo.com'
        
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

        

    def work(self):

        self.autologin()
        time.sleep(random.randint(5, 10))

        while 1:

            _imsg = manager.getwk('wk_get' if self.mod=='online' else 'wb_task')

            print _imsg
            if _imsg:

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


    # print manager.getwk('wb_task')


    # print json.loads(manager.getwk()['data'])
    # print manager.putwk({'act': 'chalou', 'p': {'mid':'4151144466717114', 'cid':'4151532825778285', 'uid': '6320271412', 'ouid':'6320271412', 'nick': '你好', 'content': '我好看吧', 'cmt_id': 0}}).content
    


    users = [

        {'username':'18479258580', 'pwd': 'hopevow110412','nickname':u'57淘券券', 'ua': 0},#0
        {'username':'zheng21aa@163.com', 'pwd': 'hopevow','nickname':u'2019的阳光', 'ua': 1},#1
        {'username':'lw100847@163.com', 'pwd': 'hopevow110412','nickname':u'有料不怕颜不好', 'ua': 2},#2
        {'username':'15070944923', 'pwd': 'hopevow110412','nickname':u'优惠券会所', 'ua': 3},#3
        {'username':'sfm0599@163.com', 'pwd': 'hopevow110412','nickname':u'爱吃榴莲的大可', 'ua': 4},#4
        {'username':'wxhjc1@163.com', 'pwd': 'hopevow110412','nickname':u'不用喝水的仙女', 'ua': 5},#5
        {'username':'zhanghongjun0121@163.com', 'pwd': 'hopevow','nickname':u'胡小小是我 ', 'ua': 6},#6
        {'username':'17069793441', 'pwd': 'hopevow','nickname':u'苍老师的小迷妹', 'ua': 7},#7
        {'username':'hopevow@sina.com', 'pwd': 'kgduucel110412','nickname':u'57点点', 'ua': 8},#8
        {'username':'17135852097', 'pwd': 'na13022','nickname':u'大眼萌萌哎睡觉','ua': 9},#9
        {'username':'17135852065', 'pwd': 'na13022','nickname':u'史上第一吃瓜群众', 'ua': 10},#10

    ]


    if len(sys.argv) >1:
        idx = int(sys.argv[1])
    else:
        idx = 0

    

    workq = Queue.Queue()

    wb = weibo(users[idx]['username'], users[idx], workq)

    if len(sys.argv) > 2:
        wb.mod = sys.argv[2]
    else:
        wb.mod = 's'

    random.shuffle(manager.sayHello)
    # print manager.getmsg().next()

    wb.work()
    # # wb.autologin()
    