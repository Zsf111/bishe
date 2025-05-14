#!/bin/bash

HIVE_DATABASE='beike'
MYSQL_DATABASE='beike_dws'
MYSQL_USER='用户名'
MYSQL_PASSWORD='密码'
MYSQL_HOST='主机'
MYSQL_PORT='端口'

TABLES=('dws_area' 'dws_district' 'dws_floor' 'dws_lift' 'dws_owner'
'dws_orient' 'dws_type')

CONNECT_STRING="jdbc:mysql://${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}?useUnicode=true&characterEncoding=UTF-8"

# 定义最大重试次数
MAX_RETRIES=3

for TABLE in "${TABLES[@]}"; do
  retry_count=0
  success=false
  
  while [ $retry_count -lt $MAX_RETRIES ] && [ $success = false ]; do
    echo "开始迁移表: ${HIVE_DATABASE}.${TABLE} 到 MySQL (尝试 $((retry_count + 1))/$MAX_RETRIES)"

    # Sqoop 导出命令
    sqoop export \
      --connect "${CONNECT_STRING}" \
      --username "${MYSQL_USER}" \
      --password "${MYSQL_PASSWORD}" \
      --table "${TABLE}" \
      --export-dir "/user/hive/warehouse/${HIVE_DATABASE}.db/${TABLE}" \
      --fields-terminated-by ',' \
      --lines-terminated-by '\n'

    if [ $? -eq 0 ]; then
      echo "表 ${HIVE_DATABASE}.${TABLE} 迁移成功"
      success=true
    else
      echo "表 ${HIVE_DATABASE}.${TABLE} 迁移失败，清空目标表数据..."
      
      # 清空目标表数据
      mysql -h${MYSQL_HOST} -P${MYSQL_PORT} -u${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE} -e "TRUNCATE TABLE ${TABLE}"
      
      retry_count=$((retry_count + 1))
      if [ $retry_count -lt $MAX_RETRIES ]; then
        echo "等待 30 秒后重试..."
        sleep 30
      else
        echo "表 ${HIVE_DATABASE}.${TABLE} 在 $MAX_RETRIES 次尝试后仍然迁移失败"
        echo "请检查错误日志并手动处理该表"
      fi
    fi
  done
done

# 检查是否所有表都迁移成功
for TABLE in "${TABLES[@]}"; do
  sqoop eval \
    --connect "${CONNECT_STRING}" \
    --username "${MYSQL_USER}" \
    --password "${MYSQL_PASSWORD}" \
    --query "SELECT COUNT(*) FROM ${TABLE}" > /dev/null 2>&1
    
  if [ $? -ne 0 ]; then
    echo "警告: 表 ${TABLE} 可能未成功迁移，请检查"
  fi
done

echo "迁移过程完成，请检查上述输出确认所有表的状态"

exit 0