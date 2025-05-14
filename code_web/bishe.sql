-- 创建数据库bishe
create database if not exists bishe;

-- 使用数据库bishe
use bishe;

-- 创建user表
create table if not exists user(
    user_id int primary key auto_increment,
    username varchar(10) not null unique,
    password char(60) not null,
    email varchar(20) not null,
    register_time datetime not null,
    profile text
);

-- 创建house表
create table if not exists house(
    house_id int primary key auto_increment,
    community_name varchar(50) not null,
    district varchar(5) not null,
    sub_district varchar(5),
    total_price float not null,
    unit_price float not null,
    house_type varchar(5),
    house_area float,
    house_struc varchar(5),
    const_type varchar(5),
    house_floor int,
    house_orient varchar(5),
    const_struc varchar(5),
    renov_condi varchar(5),
    lift_rate varchar(5),
    heat_method varchar(5),
    have_lift boolean default false,
    trans_owner varchar(5),
    house_purpo varchar(5),
    house_age varchar(5),
    prope_owner varchar(5),
    mortg_info varchar(50)
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

-- 创建admin表
create table if not exists admin(
    admin_id int primary key auto_increment,
    username varchar(20) not null unique,
    password varchar(20) not null,
    email varchar(20) not null,
    create_time datetime not null,
    last_login datetime
);

