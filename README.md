HiveMeta (restful)
====
1.Usage

RUN: `python api.py `


`[GET] http://ip:3434/[dbname]/[tablename]`

return

	{
		"columns": [
			{
			"comment": null,
			"index": 0,
			"name": "id",
			"type": "string"
			},
			{
			"comment": null,
			"index": 1,
			"name": "order_no",
			"type": "string"
			},
		],
		"database": "load",
		"partitions": [
			{
			"comment": null,
			"index": 0,
			"name": "ids",
			"type": "string"
			}
		],
		"source":"hdfs://namenode171:54310/user/hive/bi_warehouse/LOAD.db/fanli_slice_man_vi_tb_pay_orders_init",
		"table":"fanli_slice_man_vi_tb_pay_orders_init"
	}	
`[GET] http://ip:3434/tables/[dbname]`

return

	[{"table":"fanli_slice_man_vi_tb_pay_orders_init"},{"table":""}]
	
`[GET] http://ip:3434/dbpath/[dbname]`

return

	{
	"dbLocation":"hdfs://namenode171:54310/user/hive/bi_warehouse/LOAD.db"
	}

P.S.
fit for hive 0.13