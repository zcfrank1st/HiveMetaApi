# -*- coding: utf-8 -*-
__author__ = 'zcfrank1st'

from flask import Flask
from flask_restful import Resource, Api
import MySQLdb

app = Flask(__name__)
api = Api(app)

HOST = "hive.db.51fanli.it"
USER = "hive"
PASSWD = "hive@51fanli.com"
DB = "hive"
CHARSET = "utf8"


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class MetaInfo(Resource):
    def get(self, db, table):
        return self.meta_info(db, table)

    def meta_info(self, db, table):
        conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)
        cursor = conn.cursor()

        cursor.execute("select DB_ID, DB_LOCATION_URI from dbs where name = '%s'" % db)
        db_results = cursor.fetchall()
        db_id = db_results[0][0]
        db_location = db_results[0][1]

        cursor.execute("select SD_ID, TBL_ID from TBLS where TBL_NAME = '%s' and DB_ID = %d" % (table, db_id))
        r = cursor.fetchall()
        sd_id = r[0][0]
        tbl_id = r[0][1]

        cursor.execute("select CD_ID from sds where sd_id = %d" % sd_id)
        cd_id = cursor.fetchall()[0][0]

        cursor.execute("select INTEGER_IDX, COLUMN_NAME, TYPE_NAME, COMMENT from columns_v2 where cd_id = %d order by INTEGER_IDX" % cd_id)
        column_results = cursor.fetchall()
        columns = self.results_2_dict_arr(column_results)

        cursor.execute("select INTEGER_IDX, PKEY_NAME, PKEY_TYPE, PKEY_COMMENT from partition_keys where TBL_ID = %d order by INTEGER_IDX" % tbl_id)
        partition_results = cursor.fetchall()
        partitions = self.results_2_dict_arr(partition_results)

        cursor.close()
        conn.close()

        results = {"database": db, "table": table, "source": db_location + "/" + table,  "columns": columns, "partitions": partitions}
        return results

    def results_2_dict_arr(self, results):
        arr = []
        for re in results:
            new_results = {'index': re[0], 'name': re[1], 'type': re[2], 'comment': re[3]}
            arr.append(new_results)
        return arr


class Tables(Resource):
    def get(self, db):
        return self.tables(db)

    def tables(self, db):
        conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)
        cursor = conn.cursor()

        cursor.execute("select DB_ID from dbs where name = '%s'" % db)
        db_results = cursor.fetchall()
        db_id = db_results[0][0]

        cursor.execute("select TBL_ID, TBL_NAME from TBLS where DB_ID = %d" % (db_id))
        r = cursor.fetchall()

        results = []
        for e in r:
            results.append({'table': e[1]})

        return results


class DBHdfsPath(Resource):
    def get(self, db):
        return self.db_hdfs_path(db)

    def db_hdfs_path(self, db):
        conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)
        cursor = conn.cursor()

        cursor.execute("select DB_ID, DB_LOCATION_URI from dbs where name = '%s'" % db)
        db_results = cursor.fetchall()
        db_location = db_results[0][1]
        return {'dbLocation': db_location}

api.add_resource(HelloWorld, '/')
api.add_resource(MetaInfo, '/<string:db>/<string:table>')
api.add_resource(Tables, '/tables/<string:db>')
api.add_resource(DBHdfsPath, '/dbpath/<string:db>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3434, debug=True)
