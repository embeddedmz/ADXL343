# import the needed packages
import smbus
import sys
import os
import time

'''
def unsigned_byte_to_signed_byte(unsigned_byte):
    return unsigned_byte - 256 if unsigned_byte > 127 else unsigned_byte

# word = 16-bit
def unsigned_word_to_signed_word(unsigned_word):
    return unsigned_word - 65536 if unsigned_word > 32767 else unsigned_word
'''

# create a varible to handle the bus
try:
    bus = smbus.SMBus(1)
except IOError:
    print("SMBus error")
    sys.exit(1)

# constants
DEVICE_ADDR_7_BITS = 0x1D
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATA_X0 = 0x32
DATA_X1 = 0x33
DATA_Y0 = 0x34
DATA_Y1 = 0x35
DATA_Z0 = 0x36
DATA_Z1 = 0x37

range = bus.read_byte_data(DEVICE_ADDR_7_BITS, DATA_FORMAT)
sys.stdout.write('Range code : %d\n' % (range & 0x03))
time.sleep(0.05)

# Exit standby mode
# It is recommended to configure the device in standby mode and then to enable measurement mode.
bus.write_byte_data(DEVICE_ADDR_7_BITS, POWER_CTL, 0x08)
time.sleep(0.05)

#bus.write_byte_data(DEVICE_ADDR_7_BITS, POWER_CTL, 0x)

while True:
    try:
        measList = bus.read_i2c_block_data(DEVICE_ADDR_7_BITS, DATA_X0, 6)
        #print(measList)
        #sys.stdout.write('Accelerometer rcvd bytes : (%d, %d, %d, %d, %d, %d)\n' % (dataX0, dataX1, dataY0, dataY1, dataZ0, dataZ1))
        
        xAccel = (measList[1] << 8) + measList[0]
        yAccel = (measList[3] << 8) + measList[2]
        zAccel = (measList[5] << 8) + measList[4]
        
        sys.stdout.write('Accelerometer : X=%4d, Y=%4d, Z=%4d\n' % (xAccel, yAccel, zAccel))
        
        time.sleep(0.05)
        
    except KeyboardInterrupt:
        # Enter standby mode
        bus.write_byte_data(DEVICE_ADDR_7_BITS, POWER_CTL, 0x00)
        sys.exit(0)
        
    except IOError:
        print("Disconnected")
        sys.exit(1)
        