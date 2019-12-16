/*

  bright.h (read photoresistor value)

*/

#ifndef BRIGHT_H
#define BRIGHT_H

#include <avr/io.h>

int16_t lightVal;

int16_t getBrightness( uint8_t iter );

#endif
