-- 使用beike库
use beike;

-- 创建dwd_type表
create external table if not exists dwd_type(
    house_type string,
    total_price int
)
row format delimited fields terminated by ',';

-- 上传数据到dwd_type表
insert into dwd_type
select house_type,total_price from ods_house;

-- 创建dws_type表
create external table if not exists dws_type(
    house_type string,
    avg_price int
)
row format delimited fields terminated by ',';

-- 选择并导入数据到dws_type表
INSERT INTO dws_type
SELECT house_type, AVG(total_price) AS avg_price
FROM dwd_type
GROUP BY house_type;