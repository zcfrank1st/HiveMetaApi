# -*- coding: utf-8 -*-
__author__ = 'zcfrank1st'

from flask import Flask
from flask_restful import Resource, Api
import MySQLdb
import simplejson as json

app = Flask(__name__)
api = Api(app)

conn = MySQLdb.connect(host="??", user="??", passwd="??", db="??")
cursor = conn.cursor()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class MetaInfo(Resource):
    def get(self, db, table):
        return self.meta_info(db, table)

    def meta_info(self, db, table):
        cursor.excute("select DB_ID from dbs where name = '%s'" % db)
        db_id = cursor.fetchall()[0][0]

        cursor.excute("select SD_ID, TBL_ID from TBLS where TBL_NAME = '%s' and DB_ID = %d" % (table, db_id))
        sd_id = cursor.fetchall()[0][0]
        tbl_id = cursor.fetchall()[0][1]

        cursor.excute("select CD_ID from sds where sd_id = %d" % sd_id)
        cd_id = cursor.fetchall()[0][0]

        cursor.excute("select COLUMN_NAME, TYPE_NAME, COMMENT from columns_v2 where cd_id = %d" % cd_id)
        column_results = cursor.fetchall()
        columns = self.results_2_dict_arr(column_results)

        cursor.excute("select PKEY_NAME, PKEY_TYPE, PKEY_COMMENT from partition_keys where TBL_ID = %d" % tbl_id)
        partition_results = cursor.fetchall()
        partitions = self.results_2_dict_arr(partition_results)

        results = {"database": db, "table": table, "columns": columns, "partitions": partitions}

        return json.dumps(results)

    def results_2_dict_arr(self, results):
        arr = []
        for re in results:
            new_results = {'name': re[0], 'type': re[1], 'comment': re[2]}
            arr.append(new_results)
        return arr


api.add_resource(HelloWorld, '/')
api.add_resource(MetaInfo, '/<string:db>/<string:table>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3434, debug=True)
