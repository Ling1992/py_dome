create table article_list(
id int not null auto_increment comment '行号',
title varchar(10) default '' comment '标题',
abstract varchar(200) default '' comment '描述',
tag varchar(20) comment '类型',
group_id bigint comment '文章id',
original_time int comment '原时间戳',
create_date datetime not null default current_timestamp comment '入库时间',
primary key (id),
unique key idx(group_id),
index (tag(15))
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章列表';

# 文章
create table article(
article_id bigint not null comment '行号',
title varchar(255) default '' comment '标题',
article text comment '文章',
create_date datetime not null default current_timestamp comment '入库时间',
primary key (article_id)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文章';