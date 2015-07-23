HiveMeta (restful)
====
1.Usage

RUN: `python api.py `


[GET] http://ip:3434/[dbname]/[tablename]

return

hive meta json <br>

	{
    	"database" : "",
    	"table" : "",
    	"columns" : [
    	{
        	"name": "",
        	"type": "",
        	"comment": ""
    	},{
        	"name": "",
        	"type": "",
        	"comment": ""
    	},{
        	"name": "",
        	"type": "",
        	"comment": ""
    	}],
    	"partitions": [{
        	"name": "",
        	"type": "",
        	"comment": ""
    	},{
        	"name": "",
        	"type": "",
        	"comment": ""
    	}]
	}
P.S.
	
hive version 0.13

gain hive meta table info : <br>

	select DB_ID from dbs where name = ?

	select SD_ID, TBL_ID from TBLS where TBL_NAME = ? and DB_ID = ?

	select CD_ID from sds where sd_id = ?

	select COLUMN_NAME, TYPE_NAME, COMMENT from columns_v2 where cd_id = ?

	select PKEY_NAME, PKEY_TYPE, PKEY_COMMENT from partition_keys where TBL_ID = ?