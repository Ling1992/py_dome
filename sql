create table article_list(
id int not null auto_increment comment '行号',
author_id bigint not null comment '作者 id',
title varchar(100) default '' comment '标题',
abstract varchar(255) default '' comment '描述',
tag varchar(30) default '' comment '类型',
chinese_tag varchar(10) default '' comment '类型',
url varchar(100) default '' comment '文章地址url',
group_id bigint comment '文章id',
original_time datetime not null comment '原时间',
create_date datetime not null default current_timestamp comment '入库时间',
primary key (id),
unique key idx(url),
index (tag(15))
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章列表';

create table article(
id int not null auto_increment comment '行号',
author_id bigint not null comment '作者 id',
url varchar(100) default '' comment '文章地址url',
title varchar(100) default '' comment '标题',
article text comment '文章',
create_date datetime not null default current_timestamp comment '入库时间',
primary key (id),
unique key idy(url)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章';

create table author (
id bigint not null auto_increment comment '作者 id',
name varchar(40) default '' comment '名称',
media_id bigint default 0 comment 'media id',
fensi int default 0 comment '粉丝数',
guanzhu int default 0 comment '关注',
type varchar(20) default '' comment '类型',
primary key (id)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='作者';

create table author_list (
id bigint not null auto_increment comment '作者 id',
name varchar(40) default '' comment '名称',
media_id bigint default 0 comment 'media id',
fensi int default 0 comment '粉丝数',
guanzhu int default 0 comment '关注',
type varchar(20) default '' comment '类型',
primary key (id)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='作者';

create table if not exists `article_category` (
    `category_id` int not null auto_increment comment '主键 id' ,
    `name` varchar(10) default '其他' comment '类型 名称',
    `word` varchar(20) default 'other' comment '类型 英文 名称',
    primary key (`category_id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章 类型';


create table if not exists `article_list`(
    `id` int not null auto_increment comment '行号',
    `title` varchar(100) default '' comment '标题',
    `abstract` varchar(255) default '' comment '描述',
    `image_url` varchar(100) default '' comment '图片 URI',
    `create_date` datetime not null default current_timestamp comment '文章创建时间',
    `click_amount` int not null default 0 comment '点击量',

    `author_id` bigint not null comment '作者 id',
    `category_id` not null comment '类型 关联 id ',

    `article_id` bigint comment '文章id',

    primary key (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章列表';

create table if not exists toutiao_author (
    `author_id` bigint not null auto_increment comment '作者 id',
    `name` varchar(40) default '' comment '名称',
    `media_id` bigint default 0 comment '媒体 id',
    `fensi` int default 0 comment '粉丝数',
    `guanzhu` int default 0 comment '关注',
    `type` varchar(20) default '' comment '类型', /* 待处理 是否需要 author_category */
    primary key (`author_id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='头条 作者';

create table if not exists article(
    `id` int not null auto_increment comment '行号',
    `author_id` bigint not null comment '作者 id',
    `url` varchar(100) default '' comment '文章地址url',
    `title` varchar(100) default '' comment '标题',
    `article` text comment '文章',
    `create_date` datetime not null default current_timestamp comment '入库时间',
    primary key (id),
    unique key idy(url)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章';


create table if not exists pi_pool(
    `id` int not null auto_increment comment '行号',
    `ip` varchar(15) not null comment 'ip 地址',
    `port` int(5) not null comment '端口',
    `type` tinyint(1) not null default 1 comment '类型 1 http 2 https',
    `state` tinyint(1) not null default 0 comment '是否有效  0：有效 1：无效',
    primary key (id),
    unique key idy(ip)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章';

`is_hot` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否有效  0：正常 1：热门'