-- 使用beike库
use beike;

-- 创建dwd_owner表
create external table if not exists dwd_owner(
    prope_owner string,
    total_price int
)
row format delimited fields terminated by ',';

-- 上传数据到dwd_owner表
insert into dwd_owner
select prope_owner,total_price from ods_house;

-- 创建dws_owner表
create external table if not exists dws_owner(
    prope_owner string,
    avg_price int
)
row format delimited fields terminated by ',';

-- 选择并导入数据到dws_owner表
INSERT INTO dws_owner
SELECT prope_owner, AVG(total_price) AS avg_price
FROM dwd_owner
GROUP BY prope_owner;