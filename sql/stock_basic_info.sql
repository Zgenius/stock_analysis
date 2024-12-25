CREATE TABLE `stock_basic_info` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `symbol` varchar(12) NOT NULL DEFAULT '' COMMENT '股票编码',
  `name` varchar(12) NOT NULL DEFAULT '' COMMENT '股票名称',
  `sector` varchar(128) NOT NULL DEFAULT '' COMMENT '所属行业',
  `listing_time` timestamp NOT NULL COMMENT '上市日期',
  `total_share_capital` bigint unsigned  NOT NULL DEFAULT 0 COMMENT '总股本',
  `extra_info` json DEFAULT NULL COMMENT '扩展信息',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `symbol` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='股票基础信息';