import logging
import time
import serial
import datetime
import sqlite3
import logging

# create a file handler
now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

log = logging.getLogger('rssi')
fh = logging.FileHandler('rssi.log')

# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

log.addHandler(fh)
log.addHandler(console)

log.setLevel(logging.DEBUG)


from xbee import XBee
PORT = '/dev/tty.usbserial-FTF0FD46' #OSX 
# PORT = '/dev/ttyAMA0' #set tty port NOTE: ON BEAGLE BONE O1 is the Letter
BAUD_RATE = 9600 #set baud rate

serial_port = serial.Serial(PORT, BAUD_RATE)

conn = sqlite3.connect('xbee_rssi.db', detect_types=sqlite3.PARSE_DECLTYPES)

with conn:  
    cur = conn.cursor()    
    
    cur.execute("DROP TABLE IF EXISTS signal")
    log.info('Setting up Database...')
    # Create table
    cur.execute('''CREATE TABLE signal
                 (date TIMESTAMP, xbee INTEGER, rssi INTEGER)''')


def dump(data): #define callback function
    conn = sqlite3.connect('xbee_rssi.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    if 'rssi' in data: 
        print int(data['rssi'].encode('hex'),16)
    
    if 'source_addr' in data:
            addr = data['source_addr']
            print data
            rssi_val = int(data['rssi'].encode('hex'),16)
            addr_int = int(addr.encode('hex'),16)

            rf_data = "got the message (%s)" % data['rf_data']
            fid = data['options']
            log.debug('rssi value: %d from: %d' % (rssi_val,addr_int))
            
            # now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            now = datetime.datetime.now()
            
            cur.execute("INSERT INTO signal VALUES(?, ?, ?)", (now,addr_int,-1*rssi_val))
            # Save (commit) the changes
            conn.commit()

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
