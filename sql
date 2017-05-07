create table article_list(
id int not null auto_increment comment '行号',
title varchar(100) default '' comment '标题',
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
url varchar(100) default '' comment '文章地址url',
title varchar(100) default '' comment '标题',
article text comment '文章',
create_date datetime not null default current_timestamp comment '入库时间',
primary key (id),
unique key idy(url)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章';