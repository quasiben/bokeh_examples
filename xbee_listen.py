import logging
import time
import serial

import logging

log = logging.getLogger('rssi')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('rssi.log')
fh.setLevel(logging.WARNING)
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
log.addHandler(fh)


from xbee import XBee
PORT = '/dev/ttyAMA0' #set tty port NOTE: ON BEAGLE BONE O1 is the Letter
BAUD_RATE = 9600 #set baud rate

serial_port = serial.Serial(PORT, BAUD_RATE)


def dump(data): #define callback function
    if 'rssi' in data: 
        print int(data['rssi'].encode('hex'),16)
    if 'source_addr' in data:
            print 'source_addr'
            addr = data['source_addr']
            rf_data = "got the message (%s)" % data['rf_data']
            fid = data['options']
            #print "sending (", rf_data, ") back to ", str(data['source_addr'].encode("hex"))
            log.info('rssi value: %d' % int(data['rssi'].encode('hex'),16))
            xbee.send('tx', frame_id=fid, dest_addr=addr, data=rf_data)
    
serial_port = serial.Serial(PORT, BAUD_RATE)
xbee = XBee(serial_port, callback=dump, escaped=True) #asynchronous calling to 

# loop forever
while True:
    try: 
        time.sleep(0.5)
    except KeyboardInterrupt:
        break


xbee.halt()
serial_port.close()
