#!/usr/bin/env bash

startTime=`date "+%Y-%m-%d 06:00:00"`
startTimeStamp=`date -j -f '%Y-%m-%d %H:%M:%S' "$startTime" +%s`

endTime=`date "+%Y-%m-%d 23:00:00"`
endTimeStamp=`date -j -f '%Y-%m-%d %H:%M:%S' "$endTime" +%s`

currentTimeStamp=`date +%s`

if [ $currentTimeStamp -lt $startTimeStamp ] || [ $currentTimeStamp -ge $endTimeStamp ] ; then
    echo 'start'
    exit
fi

echo 'aa'