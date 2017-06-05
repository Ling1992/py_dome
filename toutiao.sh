#!/usr/bin/env bash

# 进入 项目 目录
cd /Users/ling/PycharmProjects/py_dome/ &&

# shell 日志
shlogdir='/Users/ling/PycharmProjects/py_dome/cache/sh/'
if [ ! -d $shlogdir ]
then
    echo '不存在 shell cache 目录---> 正在 创建'
    mkdir $shlogdir
fi

echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log'

# 判断 .py 是否 未 完成
var=10
while [ $var -gt 0 ]
do
    echo $var
    var=$[ $var - 1 ]
    count=`ps aux | grep toutiao2.py | grep -v grep | wc -l`
    re=`ps aux | grep toutiao2.py | grep -v grep`
    pid=`ps aux | grep toutiao2.py | grep -v grep | awk '{print $2}'`

    if [ $count -gt 1 ]
    then
        echo '存在 未完成 toutiao.py 进程 ！！进程:$pid 详情:$re' >> $shlogdir`date +%Y-%m-%d`'_run.log'
        echo '肯存在问题 请及时处理' >> $shlogdir`date +%Y-%m-%d`'_run.log'
        kill -15 $pid
    else
        break
    fi
done
echo 'start'

envpath='/Users/ling/.test1vem/bin/'
source $envpath'activate'  &&
python update_user.py  &&
python create_author.py  &&
python toutiao2.py  &&
deactivate  &&

echo '任务结束: '`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log'

# # 每小时 执行  Python
# # 0 */1 * * * /bin/sh /Users/ling/PycharmProjects/py_dome/toutiao.sh >/dev/null 2>&1