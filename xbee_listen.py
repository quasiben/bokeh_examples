import time
import serial
import datetime
import sqlite3


from xbee import XBee
import platform

PORT = ''

if platform.machine() == 'armv6l':
    PORT = '/dev/ttyAMA0' #set tty port BEAGLE BONE NOTE: O1 
else:
    if platform.system() == 'Linux':
        PORT = '/dev/ttyUSB0'
    if platform.system() == 'Darwin':
        PORT = '/dev/tty.usbserial-FTF0FD46' #OSX


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

def dump(data): #define callback function
    conn = sqlite3.connect('xbee_rssi.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    
    if 'source_addr' in data:
            addr = data['source_addr']
            rssi_val = int(data['rssi'].encode('hex'),16)
            addr_int = int(addr.encode('hex'),16)

            rf_data = "got the message (%s)" % data['rf_data']
            fid = data['options']
            
            # now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            now = datetime.datetime.now()
            
            print rssi_val
            cur.execute("INSERT INTO signal VALUES(?, ?, ?)", (now,addr_int,-1*rssi_val))
            # Save (commit) the changes
            conn.commit()

            xbee.send('tx', frame_id=fid, dest_addr=addr, data=rf_data)

    conn.close()
    
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