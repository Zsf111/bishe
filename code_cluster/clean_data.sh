#! /bin/bash

# 删除csv文件的第一行
sed -i '1d' /usr/local/data/house_clean.csv

# 查看csv文件的前5行
head -5 /usr/local/data/house_clean.csv

