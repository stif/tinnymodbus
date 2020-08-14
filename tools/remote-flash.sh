#!/bin/sh
ADDR=1

# switch into bootloader
python ./examples/mainmode-switch.py $ADDR

sleep .5

# flash over rs485 wires
./modbus-flash $ADDR ../main.hex

sleep .5

# switch back to main
python ./examples/bootmode-switch.py $ADDR

# execute a sensor read after flash
python ./examples/sensors-read.py $ADDR
