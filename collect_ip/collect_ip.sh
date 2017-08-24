#!/usr/bin/env bash

echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'` >> '/Users/ling/PycharmProjects/py_dome/collect_ip/toutiao.sh.log'

# 进入 项目 目录

cd /Users/ling/PycharmProjects/py_dome/collect_ip  &&

envpath='/Users/ling/.test1vem/bin/'  &&

source ${envpath}'activate'  &&
python collect_ip.py  &&
deactivate

# #   每晚23:30 更新  执行  collect_ip
#30 23 * * * /bin/sh /Users/ling/PycharmProjects/py_dome/collect_ip/collect_ip.sh >/Users/ling/PycharmProjects/py_dome/collect_ip/toutiao.sh.log 2>&1