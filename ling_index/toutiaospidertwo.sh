#!/usr/bin/env bash

# 进入 项目 目录
cd /Users/ling/PycharmProjects/py_dome/ling_index

# shell 日志
shlogdir='cache/sh/toutiaospidertwo/'
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

if [ ${currentTimeStamp} -ge ${startTimeStamp} ] && [ ${currentTimeStamp} -lt ${endTimeStamp} ] ; then
    echo '6点到 晚上11点 不进行任务:'`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log'
    exit
fi

echo '任务开始: '`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log'

# 判断 pid 文件
if [ -e "cache/toutiaospidertwo.pid" ]; then
    echo 'toutiaospidertwo.pid 文件已经存在 请及时处理' >> ${shlogdir}`date +%Y-%m-%d`'_run.log'
    exit
fi

echo 'start-->>'`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log'

envpath='/Users/ling/.test1vem/bin/'  &&
source ${envpath}'activate'  &&
python toutiaospidertwo.py  &&
deactivate  &&
echo '任务结束: '`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log' &&
echo -e "\n" >>${shlogdir}`date +%Y-%m-%d`'_run.log' &&

/bin/sh /Users/ling/PycharmProjects/py_dome/get_user_info.sh >/dev/null 2>&1 &&

echo 'get_user_info over: '`date +'%Y-%m-%d %H:%M:%S'` >> ${shlogdir}`date +%Y-%m-%d`'_run.log'

# # 每小时 执行  toutiaospidertwo
# # 0 */2 * * * /bin/sh /Users/ling/PycharmProjects/py_dome/ling_index/toutiaospidertwo.sh >/dev/null 2>&1