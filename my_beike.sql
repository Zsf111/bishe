-- 创建beike_dws库
create database if not exists beike_dws;

-- 使用beike_dws库
use beike_dws;

-- 创建dws_area表
create table if not exists dws_area(
    area_range varchar(20),
    avg_price int
);

-- 创建dws_district表
create table if not exists dws_district(
    district varchar(20),
    avg_price int
);

-- 创建dws_floor表
create table if not exists dws_floor(
    floor_range varchar(20),
    avg_price int
);

-- 创建dws_lift表
create table if not exists dws_lift(
    have_lift varchar(20),
    avg_price int
);

-- 创建dws_orient表
create table if not exists dws_orient(
    orient varchar(20),
    avg_price int
);

-- 创建dws_type表
create table if not exists dws_type(
    house_type varchar(20),
    avg_price int
);

-- 创建dws_owner表
create table if not exists dws_owner(
    prope_owner varchar(20),
    avg_price int
);

