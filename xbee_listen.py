import logging
import time
import serial
import datetime
import sqlite3


from xbee import XBee
# PORT = '/dev/tty.usbserial-FTF0FD46' #OSX 
PORT = '/dev/ttyAMA0' #set tty port NOTE: ON BEAGLE BONE O1 is the Letter
BAUD_RATE = 9600 #set baud rate

serial_port = serial.Serial(PORT, BAUD_RATE)

conn = sqlite3.connect('xbee_rssi.db', detect_types=sqlite3.PARSE_DECLTYPES)

with conn:  
    cur = conn.cursor()    
    
    cur.execute("DROP TABLE IF EXISTS signal")
    print 'Setting up Database...'
    # Create table
    cur.execute('''CREATE TABLE signal
                 (date TIMESTAMP, xbee INTEGER, rssi INTEGER)''')

xbee = XBee(serial_port, escaped=True) #asynchronous calling to 


while True:
    data = xbee.wait_read_frame()
    if 'source_addr' in data:
            addr = data['source_addr']
            rssi_val = int(data['rssi'].encode('hex'),16)
            addr_int = int(addr.encode('hex'),16)

	    #print rssi_val
            # now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            now = datetime.datetime.now()
            cur.execute("INSERT INTO signal VALUES(?, ?, ?)", (now,addr_int,-1*rssi_val))
	    conn.commit()
            # Save (commit) the changes
            fid = data['options']
            xbee.send('tx', frame_id=fid, dest_addr=addr, data='pong')

    time.sleep(.1)
    

xbee.halt()
serial_port.close()
