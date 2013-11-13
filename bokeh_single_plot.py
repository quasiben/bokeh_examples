# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

import numpy as np
from bokeh.plotting import *

import datetime
import sqlite3
import pandas as pd
import pandas.io.json as pjson


lower = 20
upper = 100

df = pd.io.json.read_json('http://localhost:5000/api/v1.0/slice/%d:%d' %(lower,upper))

rssi = df.rssi*-1.0
x = np.arange(len(df))
xbee_id = str(df.xbee[0])

output_file("xbee_rssi.html", title="XBee RSSI Signal")

line_plot = line(x,rssi, color="#0000FF", x_axis_type = "datetime", 
    tools="pan,zoom,resize", width=1200,height=300, title = 'Streaming RSSI Values',
    legend='XBee %s Raw' % (xbee_id))


xaxis()[0].axis_label = "Time"
yaxis()[0].axis_label = "Signal Strength"

line_snippet =  line_plot.inject_snippet()
print line_snippet

if __name__ == "__main__":
    show()  # open a browser
