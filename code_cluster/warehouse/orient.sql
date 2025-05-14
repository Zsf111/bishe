-- 使用beike库
use beike;

-- 创建dwd_orient表
create external table if not exists dwd_orient(
    house_orient string,
    total_price int
)
row format delimited fields terminated by ',';

-- 上传数据到dwd_orient表
insert into dwd_orient
select house_orient,total_price from ods_house;

-- 创建dws_orient表
create external table if not exists dws_orient(
    orient string,
    avg_price int
)
row format delimited fields terminated by ',';

-- 选择并导入数据到dws_orient表
INSERT INTO dws_orient
SELECT
  house_orient,
  AVG(total_price) AS avg_price
FROM dwd_orient
GROUP BY house_orient;

