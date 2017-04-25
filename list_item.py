# _*_ encoding:utf-8 _*_


class ListItem(object):
    abstract = None     # 描述
    image_url = None    # 缩略图
    title = None        #
    tag = None          # 类型
    chinese_tag = None  #
    source_url = None   # 文章 url
    group_id = None     # 文章 id
    has_gallery = None  # 是否 媒体资源

    def set_class(self, ob):
        self.abstract = ob.get('abstract')
        self.image_url = ob.get('image_url')
        self.title = ob.get('title')
        self.tag = ob.get('tag')
        self.chinese_tag = ob.get('chinese_tag')
        self.source_url = ob.get('source_url')
        self.group_id = ob.get('group_id')
        self.has_gallery = ob.get('has_gallery')

