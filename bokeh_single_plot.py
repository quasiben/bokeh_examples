# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

import numpy as np
from bokeh.plotting import *

import datetime
import sqlite3
import pandas as pd
import pandas.io.json as pjson
import pandas.io.sql as psql


lower = 20
upper = 100

#df = pd.io.json.read_json('http://localhost:5000/api/v1.0/slice/%d:%d' %(lower,upper))
conn = sqlite3.connect('xbee_saved.db', detect_types=sqlite3.PARSE_DECLTYPES)
sql = 'SELECT * FROM signal WHERE ROWID >= %s  AND ROWID < %s' % (lower,upper)
df = psql.read_frame(sql,conn)

rssi = df.rssi*-1.0
x = np.arange(len(df))
xbee_id = str(df.xbee[0])

output_file("xbee_rssi.html", title="XBee RSSI Signal")

line_plot = line(x,rssi, color="#0000FF", x_axis_type = "datetime",
    tools="pan,zoom,resize", width=600,height=200, title = 'Streaming RSSI Values',
    legend='XBee %s Raw' % (xbee_id), name='xbee_plot')


xaxis()[0].axis_label = "Time"
yaxis()[0].axis_label = "Signal Strength"

line_snippet =  line_plot.inject_snippet(server=False)

open("embed_example.html","w").write("""
<html>
</html>
<body>
<h1> embed example</h1>
%s
<h2> after embed </h2>

""" % line_snippet)

print line_snippet

if __name__ == "__main__":
    show()  # open a browser
