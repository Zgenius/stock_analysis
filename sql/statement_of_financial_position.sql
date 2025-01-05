CREATE TABLE `statement_of_financial_position` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `symbol` varchar(12) NOT NULL DEFAULT '' COMMENT '股票编码',
  `name` varchar(12) NOT NULL DEFAULT '' COMMENT '股票名称',
  `report_date` timestamp NOT NULL COMMENT '报告日期',
  `extra_info` json DEFAULT NULL COMMENT '扩展信息',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `symbol_reportdate` (`symbol`, `report_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='资产负债表';