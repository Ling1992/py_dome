#!/usr/bin/env bash

# 进入 run.sh 目录
cd /Users/ling/PycharmProjects/py_dome/ &&

# shell 日志
shlogdir='/Users/ling/PycharmProjects/py_dome/cache/sh/author/'
if [ ! -d $shlogdir ]
then
    echo '不存在 shell cache 目录---> 正在 创建'
    mkdir $shlogdir
fi

startTime=`date "+%Y-%m-%d 06:00:00"`
startTimeStamp=`date -j -f '%Y-%m-%d %H:%M:%S' "$startTime" +%s`

endTime=`date "+%Y-%m-%d 23:00:00"`
endTimeStamp=`date -j -f '%Y-%m-%d %H:%M:%S' "$endTime" +%s`

currentTimeStamp=`date +%s`

if [ $currentTimeStamp -ge $startTimeStamp ] && [ $currentTimeStamp -lt $endTimeStamp ] ; then
    echo '6点到 晚上11点 不进行任务:'`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log'
    exit
fi

echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log'

# 判断 .py 是否 未 完成
var=10
while [ $var -gt 0 ]
do
    echo $var
    var=$[ $var - 1 ]
    count=`ps aux | grep toutiao.py | grep -v grep | wc -l`
    re=`ps aux | grep toutiao.py | grep -v grep`
    pid=`ps aux | grep toutiao.py | grep -v grep | awk '{print $2}'`

    if [ $count -gt 1 ]
    then
        echo '存在 未完成 toutiao.py 进程 ！！进程:$pid 详情:$re' >> $shlogdir`date +%Y-%m-%d`'_run.log'
        echo '肯存在问题 请及时处理' >> $shlogdir`date +%Y-%m-%d`'_run.log'
        kill -15 $pid
    else
        break
    fi
done

# 进入 py_demo 目录
cd /Users/ling/PycharmProjects/py_dome/  &&

if [ -e cache/toutiao_news_hot_cookies.txt ]
then
    rm cache/*_cookies.txt
fi

envpath='/Users/ling/.test1vem/bin/'
source $envpath'activate'  &&
python /Users/ling/PycharmProjects/py_dome/toutiao.py  &&
deactivate  &&

echo '任务结束: '`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log' &&
echo "\n" >> $shlogdir`date +%Y-%m-%d`'_run.log'

## 每小时 执行 spider Python
# 0 */1 * * * /bin/sh /Users/ling/PycharmProjects/py_dome/toutiao.sh >/dev/null 2>&1