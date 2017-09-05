#!/usr/bin/env bash

echo $BASH_SOURCE

filename=$(basename "$BASH_SOURCE")
echo ${filename}
extension="${filename##*.}" # 删掉最后一个 .  及其左边的字符串
filename="${filename%.*}"   # 删掉最后一个 .  及其右边的字符串

tips="
    use info:\n
    ${filename}.${extension} start\n
    ${filename}.${extension} stop\n
";
opts=("start", "stop")

if [ ${#} -ne 1 ];then
    echo -e ${tips}
fi