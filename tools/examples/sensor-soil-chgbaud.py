#!/usr/bin/python

"""

  sensor-soil-chgbaud.py (Change modbus slave address)

"""

import sys
import logging

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import time


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

try:
  oldbaud = int(sys.argv[1])
  newbaud = int(sys.argv[2])
except:
  print ("usage: %s [oldbaud] [newbaud]" % sys.argv[0])
  sys.exit(-1)

baud = 0x0005 # 5 means 38400; 4 is 19200 = default

if oldbaud == 4:
  client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200, timeout=1.5) # default baud rate of soil moisture sensor
elif oldbaud == 5:
  client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=38400, timeout=1.5)

client.connect()


print ("modbus cmd: 0x04 addr: 0x0001 value: 0x%02x length: 0x02\n" % newbaud)
result  = client.write_register(address=0x0001, value=newbaud, count=0x02, unit=1)
#rq = client.write_register(1, newbaud, unit=1)

client.close()
time.sleep(1)   # Delays for 5 seconds. You can also use a float value.

if newbaud == 4:
  client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200, timeout=1.5)
elif newbaud == 5:
  client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=38400, timeout=1.5)
client.connect()
rr = client.read_holding_registers(1, 2, unit=1)
print (rr.registers[0])

print ("")

client.close()
