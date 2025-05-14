-- 使用beike库
use beike;

-- 创建dwd_floor表
create external table if not exists dwd_floor(
    house_floor int,
    total_price int
)
row format delimited fields terminated by ',';

-- 上传数据到dwd_floor表
insert into dwd_floor
select house_floor,total_price from ods_house;

-- 创建dws_floor表
create external table if not exists dws_floor(
    floor_range string,
    avg_price int
)
row format delimited fields terminated by ',';

-- 选择并导入数据到dws_floor表
INSERT INTO dws_floor
SELECT
  CASE 
    WHEN house_floor < 5 THEN '1-5层'
    WHEN house_floor BETWEEN 5 AND 10 THEN '5-10层'
    WHEN house_floor BETWEEN 10 AND 15 THEN '10-15层'
    WHEN house_floor BETWEEN 15 AND 20 THEN '15-20层'
    WHEN house_floor BETWEEN 20 AND 25 THEN '20-25层'
    WHEN house_floor BETWEEN 25 AND 30 THEN '25-30层'
    ELSE '30层以上'
  END AS floor_range,
  AVG(total_price) AS avg_price
FROM dwd_floor
GROUP BY 
CASE 
    WHEN house_floor < 5 THEN '1-5层'
    WHEN house_floor BETWEEN 5 AND 10 THEN '5-10层'
    WHEN house_floor BETWEEN 10 AND 15 THEN '10-15层'
    WHEN house_floor BETWEEN 15 AND 20 THEN '15-20层'
    WHEN house_floor BETWEEN 20 AND 25 THEN '20-25层'
    WHEN house_floor BETWEEN 25 AND 30 THEN '25-30层'
    ELSE '30层以上'
  END;

