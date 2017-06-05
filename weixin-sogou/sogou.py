# -*- coding: utf-8 -*-
import requests


if __name__ == '__main__':
    response = requests.get('http://weixin.sogou.com/')
    print response.status_code, response.reason
    if response and response.status_code == 200:
        with open('weixin-sogou-com.html', 'w') as f:
            f.write(response.content)
    pass

