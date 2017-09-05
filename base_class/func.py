# _*_ encoding=utf-8 _*_
import re
import json
import HTMLParser
from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding("utf8")


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
