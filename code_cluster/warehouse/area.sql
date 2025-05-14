-- 使用beike库
use beike;

-- 创建dwd_area表
create external table if not exists dwd_area(
    house_area float,
    total_price int
)
row format delimited fields terminated by ',';

-- 上传数据到dwd_area表
insert into dwd_area
select house_area,total_price from ods_house;

-- 创建dws_area表
create external table if not exists dws_area(
    area_range string,
    avg_price int
)
row format delimited fields terminated by ',';

-- 选择并导入数据到dws_area表

INSERT INTO dws_area
SELECT
  CASE 
    WHEN house_area < 40 THEN '小于40平米'
    WHEN house_area BETWEEN 40 AND 60 THEN '40-60平米'
    WHEN house_area BETWEEN 60 AND 80 THEN '60-80平米'
    WHEN house_area BETWEEN 80 AND 100 THEN '80-100平米'
    WHEN house_area BETWEEN 100 AND 120 THEN '100-120平米'
    WHEN house_area BETWEEN 120 AND 150 THEN '120-150平米'
    WHEN house_area BETWEEN 150 AND 200 THEN '150-200平米'
    ELSE '200平米以上'
  END AS area_range,
  AVG(total_price) AS avg_price
FROM
  dwd_area
GROUP BY
  CASE 
    WHEN house_area < 40 THEN '小于40平米'
    WHEN house_area BETWEEN 40 AND 60 THEN '40-60平米'
    WHEN house_area BETWEEN 60 AND 80 THEN '60-80平米'
    WHEN house_area BETWEEN 80 AND 100 THEN '80-100平米'
    WHEN house_area BETWEEN 100 AND 120 THEN '100-120平米'
    WHEN house_area BETWEEN 120 AND 150 THEN '120-150平米'
    WHEN house_area BETWEEN 150 AND 200 THEN '150-200平米'
    ELSE '200平米以上'
  END;