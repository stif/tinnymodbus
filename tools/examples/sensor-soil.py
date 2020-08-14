#!/usr/bin/python
"""#!/home/stif/.platformio/penv/bin/python"""



"""

  sensor-read.py (Query all sensors values)

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

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=38400, timeout=1.5)
#client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=19200, timeout=1.5)
client.connect()

idslave = 0x01

if len(sys.argv) == 2:
  try:
    idslave = int(sys.argv[1])
  except:
    print ("usage: %s [idslave]" % sys.argv[0])
    sys.exit(-1)
"""
print ("0x03 0x0000\n")
result  = client.read_holding_registers(address=0x0000, count=0x02, unit=idslave)
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
print (decoder.decode_16bit_int(), " running mode\n")

print ("")

print ("0x03 0x0001\n")
result  = client.read_holding_registers(address=0x0001, count=0x02, unit=idslave)
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
x = decoder.decode_32bit_int()
print (''.join(chr((x>>8*(4-byte-1))&0xFF) for byte in range(4)) , " software version \n")
"""

try:
  print ("")

  print ("0x04 0x0000\n")
  result  = client.read_input_registers(address=0x0000, count=0x02, unit=idslave)
  decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
  val = float(decoder.decode_16bit_int())
  print (" %.2f (moisture)" % (val))

  print ("")

  print ("0x04 0x0001\n")
  result  = client.read_input_registers(address=0x0001, count=0x02, unit=idslave)
  decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
  val = float(decoder.decode_16bit_int())
  print (" %.2f C (temp)" % (val/10))


  print ("")

except:

  print ("No Soil Moisture Sensor found.")


client.close()
