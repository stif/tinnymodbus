#https://stackoverflow.com/questions/26779095/pymodbus-rtu-server-handle-requests

store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0x0]*10000),
    co = ModbusSequentialDataBlock(0, [0x0]*10000),
    hr = ModbusSequentialDataBlock(0, [0x0]*10000),
    ir = ModbusSequentialDataBlock(0, [0x0]*10000))
context = ModbusServerContext(slaves=store, single=True)

StartSerialServer(context, port='/dev/ttyUSB0', framer=ModbusRtuFramer)

class MyData(ModbusSequentialDataBlock):
    def __init__(self, address, values):
        self.address = address
        self.values = values

    def validate(self, address, count=1):
        print "validate"

    def getValues(self, address, count=1):
        print "getValues"
        print address

    def setValues(self, address, count=1):
        print "setValues"
        print address