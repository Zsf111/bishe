-- 使用beike库
use beike;

-- 创建dwd_lift表
create external table if not exists dwd_lift(
    have_lift string,
    total_price int
)
row format delimited fields terminated by ',';

-- 上传数据到dwd_lift表
insert into dwd_lift
select have_lift,total_price from ods_house;

-- 创建dws_lift表
create external table if not exists dws_lift(
    have_lift string,
    avg_price int
)
row format delimited fields terminated by ',';

-- 选择并导入数据到dws_lift表
INSERT INTO dws_lift
SELECT have_lift, AVG(total_price) AS avg_price
FROM dwd_lift
GROUP BY have_lift;
