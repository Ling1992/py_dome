# _*_ encoding=utf-8 _*_
import re
import json
import random
import HTMLParser
from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding("utf8")

agent = [
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
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]


def get_article_one(content, key_one, key_two):   # # js中 articleInfo: { content: '...
    res = get_js_obj(content, key_one)
    # 排除 \' 影响 ！！
    res = re.sub(r'\\\'', '`', res)
    res = get_js_obj(res, key_two, r"%s[\s]*[=:][\s]*'(?:(?!')[\s\S])+'" % key_two)
    # 获取 内容
    res = get_js_obj(res, key_two, r"'(?:(?!')[\s\S])+'")
    res = re.sub(r'\'', '', res)  # # 去除 ''
    html_parser = HTMLParser.HTMLParser()   # # html 转义
    res = html_parser.unescape(res)
    return res


def get_article_two(content, key_one, key_two=None):  # # js 中 的 json
    res = get_js_obj(content, key_one)
    if key_two:
        res = get_js_obj(res, key_two)
    res = get_json_obj(res)
    return res


def get_js_obj(content, key, reg=None):
    # # 结尾可以是 } 或者 }; 所有用 </script> 做更大范围的检索
    res = ""
    if reg is None:
        reg = r"%s[\s]*[=:][\s]*{(?:(?!</script>)(?!};)[\s\S])+(})" % key
    s = re.search(reg, content)
    # if not content:
    #     return res
    if s:
        res = s.group()
    else:
        # res = content
        print key, " 匹配 失败 "
    return res


def get_json_obj(string_1):
    if not string_1:
        return string_1
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


def get_article(response, params):
    text = unicode(response.content, encoding='utf-8')  # 解决乱码问题
    dom = pq(text).make_links_absolute(response.url)
    content = ''
    if params['article_genre'] == "gallery":
        content_obj = get_article_two(dom.html(), "galleryInfo", "gallery")
        if not content_obj:
            content_obj = get_article_two(dom.html(), "gallery")
        if content_obj:
            try:
                sub_images = content_obj['sub_images']
                sub_abstracts = content_obj['sub_abstracts']
                for a in range(len(sub_images)):
                    content = content + "<p>&darr;{0}</p>\n<p><img src=\"{1}\" alt=\"{2}\"/></p>\n".format(
                        sub_abstracts[a], sub_images[a]['url'], params.get("title"))
                content = "<div>\n{}</div>\n".format(content)
            except Exception, e:
                print "error !! content_obj -> div :", e.message
        else:
            figures = dom('figure')
            if figures:
                for figure in figures.items():
                    print figure.find('img')
                    content = content + "<p>&darr;{0}</p>\n<p><img src=\"{1}\" alt=\"{2}\"/></p>\n".format(
                        figure.text(), figure.find('img').attr('alt-src'), params.get("title"))
                content = "<div>\n{}</div>\n".format(content)
            else:
                print 'error: article_genre == gallery  --> search nothing :', response.content
        pass
    else:
        content = get_article_one(dom.html(), 'articleInfo', 'content')
        if not content or not len(content):
            print(u"find -->content 1")
            content = dom.find(".article-content").html()

        if not content or not len(content):
            print(u"find -->content 2")
            content = dom('article').html()

        if not content or not len(content):
            print(u"find -->content 3")
            content = dom.find('.article-main').html()

        if not content or not len(content):
            print(u"find -->content 4")
            content = dom.find('.rich_media_content').html()

        if not content or not len(content):
            print(u"find -->content 5")
            content = dom.find(".text").html()

        if not content or not len(content):
            print(u"find -->content 6")
            content = dom.find(".contentMain").html()

        if not content or not len(content):
            print(u"find -->content 7")
            content = dom.find('.textindent2em').html()

        if not content or not len(content):
            print(u"find -->content 8")
            content = dom.find('.f14').html()

        if not content or not len(content):
            print(u"find -->content 9")
            content = dom.find('.m-detail-bd').html()

        if not content or not len(content):
            print(u"find -->content 10")
            content = dom.find('.artical-content').html()
    return content


def strtoint(time_str):
    time_str = time_str.replace('秒', '')
    time_str = time_str.replace('分钟', '')
    time_str = time_str.replace('分', '')
    time_str = time_str.replace('小时', '')
    return eval(time_str)


def strtosecond(time_str):
    if time_str:
        if '秒' in time_str:
            return strtoint(time_str)
        elif '分' in time_str or '分钟' in time_str:
            return strtoint(time_str) * 60
        elif '小时' in time_str:
            return strtoint(time_str) * 60 * 60
        else:
            return 10000
    else:
        return 0


def ydl_collect_ip(html, callback):
    dom = pq(html)
    trs = dom('tbody')('tr')

    for tr in trs.items():
        tds = tr('td')
        data = {}
        j = 0
        for td in tds.items():
            if j == 0:
                data['ip'] = td.html()
            elif j == 1:
                data['port'] = td.html()
            elif j == 3:
                if td.html() == u'HTTP':
                    data['type'] = 1
                else:
                    data['type'] = 2
            elif j == 6:
                connect_time = strtosecond(td.html())
                if connect_time > 5:
                    data = {}
                    break
            j += 1
        if data:
            callback(data)
    pass


def kdl_collect_ip(html, callback):
    pass


def xcdl_collect_ip(html, callback):
    if html:
        dom = pq(html)
        trs = dom('table')('tr')
        i = 0
        for tr in trs.items():
            i += 1
            if i == 1:
                continue
            else:
                tds = tr('td')
                data = {}
                j = 0
                for td in tds.items():
                    j += 1
                    if j == 2:
                        data['ip'] = td.html()
                    if j == 3:
                        data['port'] = td.html()
                    if j == 6:
                        if td.html() == u'HTTP':
                            data['type'] = 1
                        else:
                            data['type'] = 2
                    if j == 7:
                        race = strtosecond(td('div').attr('title'))
                        if race > 5:
                            data = {}
                            continue
                    if j == 8:
                        connect_time = strtosecond(td('div').attr('title'))
                        if connect_time > 5:
                            data = {}
                            continue
                    if j == 9:
                        effective_time = strtosecond(td.html())
                        if effective_time <= 120:
                            data = {}
                            continue
                if data:
                    callback(data)
                    # print data
                    # print '-' * 88
        pass


def get_random_agent():
    return random.choice(agent)


def check_ip_exception(e):
    str_error = str(e.message)
    if "ConnectTimeoutError" in str_error:
        return True
    if "[Errno 60] Operation timed out" in str_error:
        return True
    if "[Errno 61] Connection refused" in str_error:
        return True
    # if "Connection aborted" in str_error:
    #     return True
    return False

