##RPi

## Requriements:
 - pyserial
 - xbee
 - flask
 - flask-restful
 - bokeh
 - pandas
 - numpy

##RPi Side

 - run flask server
  - `python api.py`
 - start xbee on RPi or other device
  - `python xbee_listen.py`
 - start bokeh server and plotting routine:
  - `bokeh-server`
  - `python bokeh_plots.py`




##GIF Conversion: 
`ffmpeg -i input.mov -s 800x400 -pix_fmt rgb24 -r 10 -f gif - | gifsicle --optimize=3 --delay=3 > out.gif`