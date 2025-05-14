#!/bin/bash

# 设置错误时退出
set -e

echo "开始执行数据处理流程..."

# 1. 运行clean_data.sh清洗数据
echo "步骤1: 清洗数据"
sh clean_data.sh
if [ $? -ne 0 ]; then
    echo "数据清洗失败"
    exit 1
fi

# 2. 循环运行warehouse目录下的hive sql文件
echo "步骤2: 执行Hive SQL文件"
for sql_file in warehouse/*.sql
do
    echo "正在执行: $sql_file"
    hive -f "$sql_file"
    if [ $? -ne 0 ]; then
        echo "执行 $sql_file 失败"
        exit 1
    fi
done

# 3. 运行MySQL文件
echo "步骤3: 执行MySQL文件"
mysql -uroot -p1234 < my_beike.sql
if [ $? -ne 0 ]; then
    echo "执行MySQL文件失败"
    exit 1
fi

# 4. 运行数据传输脚本
echo "步骤4: 传输数据"
sh trans_data.sh
if [ $? -ne 0 ]; then
    echo "数据传输失败"
    exit 1
fi

echo "所有步骤执行完成!"