#!/usr/bin/env bash

# 进入 项目 目录
cd /Users/ling/PycharmProjects/py_dome/

# shell 日志
shlogdir='/Users/ling/PycharmProjects/py_dome/cache/sh/get_user_info/'
if [ ! -d $shlogdir ]
then
    echo '不存在 shell cache 目录---> 正在 创建'
    mkdir $shlogdir
fi

echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log'

# 判断 pid 文件
if [ -e "cache/get_user_info.pid" ]; then
    echo 'get_user_info.pid 文件已经存在 请及时处理' >> ${shlogdir}`date +%Y-%m-%d`'_run.log'
    exit
fi

echo 'start-->>'`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log'

envpath='/Users/ling/.test1vem/bin/'  &&
source ${envpath}'activate'  &&
python get_user_info.py  &&
deactivate  &&
echo '任务结束: '`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log' &&
echo -e "\n" >>${shlogdir}`date +%Y-%m-%d`'_run.log'


# 每周一的1 : 01  启动
# 01 1 * * 6,0 /bin/sh /Users/ling/PycharmProjects/py_dome/get_user_info.sh >/dev/null 2>&1