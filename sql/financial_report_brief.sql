CREATE TABLE `financial_report_brief` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `symbol` varchar(12) NOT NULL DEFAULT '' COMMENT '股票编码',
  `name` varchar(12) NOT NULL DEFAULT '' COMMENT '股票名称',
  `report_time` timestamp NOT NULL COMMENT '报告日期',
  `operating_revenue` double(20, 6) NOT NULL DEFAULT 0.0 COMMENT '营业收入',
  `net_profit` double(20, 6) NOT NULL DEFAULT 0.0 COMMENT '净利润',
  `net_asset_value_per_share` double(20, 6) NOT NULL DEFAULT 0.0 COMMENT '每股净资产',
  `earnings_per_share` double(20, 6) NOT NULL DEFAULT 0.0 COMMENT '每股收益',
  `operating_cash_flow_per_share` double(20, 6) NOT NULL DEFAULT 0.0 COMMENT '每股经营现金流量',
  `return_on_equity` double(20, 6) NOT NULL DEFAULT 0.0 COMMENT '净资产收益率',
  `gross_profit_ratio` double(20, 6) NOT NULL DEFAULT 0.0 COMMENT '销售毛利率',
  `extra_info` json DEFAULT NULL COMMENT '扩展信息',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `symbol_reporttime` (`symbol`, `report_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='股票财报摘要';