-- 创建数据库bishe
create database if not exists bishe;

-- 使用数据库bishe
use bishe;

-- 创建user表
create table if not exists user(
    user_id int primary key auto_increment,
    username varchar(20) not null,
    password varchar(255) not null,
    email varchar(25) not null,
    register_time datetime not null,
    profile text
);

-- 创建house表
create table if not exists house(
    house_id int primary key auto_increment,
    community_name varchar(100) not null,
    district varchar(50) not null,
    sub_district varchar(50),
    total_price float not null,
    unit_price float not null,
    house_type varchar(50),
    house_area float,
    house_struc varchar(50),
    const_type varchar(50),
    house_floor int,
    house_orient varchar(50),
    const_struc varchar(50),
    renov_condi varchar(50),
    lift_rate varchar(50),
    heat_method varchar(50),
    have_lift boolean default false,
    trans_owner varchar(50),
    house_purpo varchar(50),
    house_age varchar(50),
    prope_owner varchar(50),
    mortg_info varchar(100)
);

-- 创建favorite表
create table if not exists favorite(
    fav_id int primary key auto_increment,
    user_id int,
    house_id int,
    favorite_time datetime not null,
    foreign key (user_id) references user(user_id),
    foreign key (house_id) references house(house_id)
);

-- 创建history表
create table if not exists history(
    view_id int primary key auto_increment,
    user_id int,
    house_id int,
    view_time datetime not null,
    foreign key (user_id) references user(user_id),
    foreign key (house_id) references house(house_id)
);

