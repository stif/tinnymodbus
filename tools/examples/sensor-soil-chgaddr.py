#!/usr/bin/python

"""

  sensor-soil-chgaddr.py (Change modbus slave address)

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

# create connection (main mode is 38400)
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=38400, timeout=1.5)
#client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200, timeout=1.5) # default baud rate of soil moisture sensor
client.connect()

try:
  slvaddr = int(sys.argv[1])
  newaddr = int(sys.argv[2])
except:
  print ("usage: %s [slvaddr] [newaddr]" % sys.argv[0])
  sys.exit(-1)


print ("modbus cmd: 0x04 addr: 0x0000 value: 0x%02x length: 0x02\n" % newaddr)
result  = client.write_register(address=0x0000, value=newaddr, count=0x02, unit=slvaddr)
print (result)

print ("")

client.close()
