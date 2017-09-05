#!/usr/bin/env bash

# 进入 项目 目录
cd /Users/ling/PycharmProjects/py_dome/ &&

# shell 日志
shlogdir='/Users/ling/PycharmProjects/py_dome/cache/sh/author2/'
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

if [ $currentTimeStamp -lt $startTimeStamp ] || [ $currentTimeStamp -ge $endTimeStamp ] ; then
    echo '晚上11点到 凌晨6点 不进行任务:'`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log'
    exit
fi


echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log'

# 判断 .py_class 是否 未 完成
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
        echo '存在 未完成 toutiao.py_class 进程 ！！进程:$pid 详情:$re' >> $shlogdir`date +%Y-%m-%d`'_run.log'
        echo '肯存在问题 请及时处理' >> $shlogdir`date +%Y-%m-%d`'_run.log'
        kill -15 $pid
    else
        echo 'start'

        envpath='/Users/ling/.test1vem/bin/'
        source $envpath'activate'  &&
        python update_user.py  &&
        python create_author.py  &&
        python toutiao2.py  &&
        deactivate  &&
        echo '任务结束: '`date +'%Y-%m-%d %H:%M:%S'` >> $shlogdir`date +%Y-%m-%d`'_run.log' &&
        echo "\n" >>$shlogdir`date +%Y-%m-%d`'_run.log' &&
        break
    fi
done
# # 每小时 执行  Python
# # 0 */1 * * * /bin/sh /Users/ling/PycharmProjects/py_dome/toutiao2.sh >/dev/null 2>&1