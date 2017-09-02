# _*_ encoding=utf-8 _*_
import re
import HTMLParser


def get_article_one(content, key_one, key_two):   # # js中 articleInfo: { content: '...
    res = ""
    s = re.search(r"%s[\s]*[=:][\s]*{(?:(?!};)[\s\S])+(};)" % key_one, content)  # # 匹配 {}；
    if s:
        res = s.group()
    else:
        print key_one, " 匹配 失败 "

    # 排除 \' 影响 ！！
    res = re.sub(r'\\\'', '`', res)
    s = re.search(r"%s[\s]*[=:][\s]*'(?:(?!')[\s\S])+'" % key_two, res)  # # 匹配 ''
    if s:
        res = s.group()
    else:
        print key_two, " 匹配 失败 "

    # 获取 内容
    s = re.search(r"'(?:(?!')[\s\S])+'", res)  # # 匹配 {}；
    if s:
        res = s.group()
    else:
        print "1 匹配 失败 "
    res = re.sub(r'\'', '', res)
    html_parser = HTMLParser.HTMLParser()
    txt = html_parser.unescape(res)
    return txt


def get_article_two(content, key):  # # js 中 的 json
    res = ""
    s = re.search(r"%s[\s]*[=:][\s]*{(?:(?!};)[\s\S])+(};)" % key, content)  # # 匹配 {}；
    if s:
        res = s.group()
    else:
        print key, " 匹配 失败 "
