#!/usr/bin/env bash

# 进入 项目 目录
cd /Users/ling/PycharmProjects/py_dome/ling_index

# shell 日志
shlogdir='cache/sh/toutiao/'
if [ ! -d ${shlogdir} ]
then
    echo '不存在 shell cache 目录---> 正在 创建'
    mkdir ${shlogdir}
fi

startTime=`date "+%Y-%m-%d 06:00:00"`
startTimeStamp=`date -j -f '%Y-%m-%d %H:%M:%S' "$startTime" +%s`

endTime=`date "+%Y-%m-%d 23:00:00"`
endTimeStamp=`date -j -f '%Y-%m-%d %H:%M:%S' "$endTime" +%s`

currentTimeStamp=`date +%s`

if [ ${currentTimeStamp} -lt ${startTimeStamp} ] || [ ${currentTimeStamp} -ge ${endTimeStamp} ] ; then
    echo '晚上11点到 凌晨6点 不能启动任务:'`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log'
    exit
fi

echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log'

envpath='/Users/ling/.test1vem/bin/'  &&
source ${envpath}'activate'  &&
python toutiao.py  &&
deactivate  &&
echo '任务结束: '`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log' &&
echo -e "\n" >>${shlogdir}`date +%Y-%m-%d`'_run.log'

# 每5分钟 执行  toutiao
# */5 * * * * /bin/sh /Users/ling/PycharmProjects/py_dome/ling_index/toutiao.sh >/dev/null >/Users/ling/PycharmProjects/py_dome/ling_index/toutiao_sh.log 2>&1