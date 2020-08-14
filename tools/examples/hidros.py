#!/usr/bin/python

"""

  hidros.py (query and set Humidity)

"""

import sys
import logging

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# create connection
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, stopbits = 1, parity = 'N', bytesize= 8, timeout=1.5)
client.connect()

idslave = 0x01

if len(sys.argv) == 2:
  try:
    idslave = int(sys.argv[1])
  except:
    print ("usage: %s [idslave]" % sys.argv[0])
    sys.exit(-1)


print ("0x03 0xF440\n")
result  = client.read_holding_registers(address=0xF440, count=0x01, unit=idslave)
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
print (decoder.decode_bits(), " on off\n")

print ("0x03 0xF123\n")
result  = client.read_holding_registers(address=0xF123, count=0x01, unit=idslave)
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
print (decoder.decode_16bit_int(), " temperatur\n")

print ("")

client.close()
