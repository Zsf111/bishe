-- 使用beike库
use beike;

-- 创建dwd_district表
create external table if not exists dwd_district(
    district string,
    total_price int
)
row format delimited fields terminated by ',';

-- 上传数据到dwd_district表
insert into dwd_district
select district,total_price from ods_house;

-- 创建dws_district表
create external table if not exists dws_district(
    district string,
    avg_price int
)
row format delimited fields terminated by ',';

-- 选择并导入数据到dws_district表
INSERT INTO dws_district
SELECT
  district,
  AVG(total_price) AS avg_price
FROM dwd_district
GROUP BY district;

