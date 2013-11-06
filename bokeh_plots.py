# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

import numpy as np
from bokeh.plotting import *

import datetime
import sqlite3
import pandas as pd
import pandas.io.json as pjson

df = pd.io.json.read_json('http://localhost:5000/api/v1.0/80')
rssi = df.rssi*-1.0
x = np.arange(len(df))
xbee_id = str(df.xbee[0])

output_server("XBee RSSI Signal")
line(x,rssi, color="#0000FF", x_axis_type = "datetime", 
    tools="pan,zoom,resize", width=1200,height=300, title = 'Streaming RSSI Values',
    legend='XBee %s Raw' % (xbee_id))


xaxis()[0].axis_label = "Time"
yaxis()[0].axis_label = "Signal Strength"

show()

i = 0
import time
from bokeh.objects import GlyphRenderer
renderer = [r for r in curplot().renderers if isinstance(r, GlyphRenderer)][0]
ds = renderer.data_source
while True:
    df = pd.io.json.read_json('http://localhost:5000/api/v1.0/80')
    ds.data["x"] = x+80*i
    ds.data["y"] = df.rssi
    ds._dirty = True
    session().store_obj(ds)
    time.sleep(.5)
    i+=1
