from flask import Flask, jsonify
from flask.ext import restful
from flask import g #sqlite connection

import sqlite3

import datetime
import sqlite3

import platform

app = Flask(__name__)
api = restful.Api(app)

DATABASE = 'xbee_saved.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    return db


@app.route('/')
def index():
    return "Data is at: <b>/api/v1.0/INTEGER</b>"


class Count(restful.Resource):
        def get(self):
            cur = get_db().cursor()
            sql = 'SELECT COUNT(*) FROM signal' 
            cur.execute(sql)
            result =  cur.fetchall()[0][0]
            
            result_dict = {'total':result}
            return jsonify(result_dict)

if platform.machine() == 'armv6l':
    class RSSIData(restful.Resource):
        def get(self,update_lim):
            cur = get_db().cursor()
            sql = 'SELECT * FROM signal ORDER BY date DESC LIMIT %s' % (update_lim)
            cur.execute(sql)
            result =  cur.fetchall()
            date = []
            xbee = []
            rssi = []

            for pt in result:
                    date.append(pt[0])
                    xbee.append(pt[1])
                    rssi.append(pt[2]) 

            #df = psql.read_frame(sql,conn)
            result_dict = {'date':date,'rssi':rssi,'xbee':xbee}
            return jsonify(result_dict)
else:
    import pandas as pd
    import pandas.io.sql as psql


    class RSSIData(restful.Resource):
        def get(self,update_lim):
            conn = get_db()
            sql = 'SELECT * FROM signal ORDER BY date DESC LIMIT %s' % (update_lim)
            df = psql.read_frame(sql,conn)
            return jsonify(df.to_dict())

    class RSSIDataSlice(restful.Resource):
        def get(self,lowerupper):
            lower,upper = lowerupper.split(':')
            print lower, upper
            lower = str(int(lower)+1)
            conn = get_db()
            sql = 'SELECT * FROM signal WHERE ROWID >= %s  AND ROWID < %s' % (lower,upper)
            df = psql.read_frame(sql,conn)
            return jsonify(df.to_dict())




api.add_resource(Count, '/api/v1.0/count')
api.add_resource(RSSIData, '/api/v1.0/<string:update_lim>')
api.add_resource(RSSIDataSlice, '/api/v1.0/slice/<string:lowerupper>')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
