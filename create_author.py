# _*_ encoding=utf-8 _*_
from base_class.ling_mysql import MysqlLing

if __name__ == '__main__':
    ling_con = MysqlLing()
    author_list = ling_con.search("select * from author_list")
    with open('author1.txt', 'w') as f:
        for author in author_list:
            if author_list.index(author) == 0:
                pass
            else:
                f.write("\n")
            f.write(str(author['id']))

