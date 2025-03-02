-- 创建beike库
create database if not exists beike;

-- 使用beike库
use beike;

-- 创建ods_house表
create external table if not exists ods_house(
    community_name string,
    district string,
    sub_district string,
    total_price int,
    unit_price int,
    house_type string,
    house_area float,
    house_struc string,
    const_type string,
    house_floor int,
    house_orient string,
    const_struc string,
    renov_condi string,
    lift_rate string,
    heat_method string,
    have_lift string,
    trans_owner string,
    house_purpo string,
    house_age string,
    prope_owner string,
    mortg_info string
)
row format delimited fields terminated by ',';

-- 上传数据到ods_house表
load data local inpath '/usr/local/data/house_clean.csv' into table ods_house;