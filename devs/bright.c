/*

  bright.c (read photoresistor value)

*/

#include <util/delay.h>

#include "bright.h"

#define LPF_FACTOR 0.5
#define LIGHT_SENSOR_ANALOG_PIN 0

/*
DDRB |= (1 << PB3);			//replaces pinMode(PB3, OUTPUT);
DDRB |= (1 << PB4);  			//replaces pinMode(PB4, OUTPUT);
PORTB |= (1 << PB3);			//replaces digitalWrite(PB3, HIGH);
PORTB &= ~(1 << PB3);		//replaces digitalWrite(PB3, LOW);
ADMUX |= (1 << REFS0);   //use internal reference voltage of 1.1V
*/

/* ADC initialisieren */
void ADC_Init(void)
{
  // die Versorgungsspannung AVcc als Referenz wählen:
  ADMUX = (1<<REFS0);    
  // oder interne Referenzspannung als Referenz für den ADC wählen:
  // ADMUX = (1<<REFS1) | (1<<REFS0);

  // Bit ADFR ("free running") in ADCSRA steht beim Einschalten
  // schon auf 0, also single conversion
  ADCSRA = (1<<ADPS1) | (1<<ADPS0);     // Frequenzvorteiler
  ADCSRA |= (1<<ADEN);                  // ADC aktivieren

  /* nach Aktivieren des ADC wird ein "Dummy-Readout" empfohlen, man liest
     also einen Wert und verwirft diesen, um den ADC "warmlaufen zu lassen" */

  ADCSRA |= (1<<ADSC);                  // eine ADC-Wandlung 
  while (ADCSRA & (1<<ADSC) ) {         // auf Abschluss der Konvertierung warten
  }
  /* ADCW muss einmal gelesen werden, sonst wird Ergebnis der nächsten
     Wandlung nicht übernommen. */
  (void) ADCW;
}

/* ADC Einzelmessung */
uint16_t ADC_Read( uint8_t channel )
{
  // Kanal waehlen, ohne andere Bits zu beeinflußen
  ADMUX = (ADMUX & ~(0x1F)) | (channel & 0x1F);
  ADCSRA |= (1<<ADSC);            // eine Wandlung "single conversion"
  while (ADCSRA & (1<<ADSC) ) {   // auf Abschluss der Konvertierung warten
  }
  return ADCW;                    // ADC auslesen und zurückgeben
}

/* ADC Mehrfachmessung mit Mittelwertbbildung */
/* beachte: Wertebereich der Summenvariablen */
uint16_t ADC_Read_Avg( uint8_t channel, uint8_t nsamples )
{
  uint32_t sum = 0;

  for (uint8_t i = 0; i < nsamples; ++i ) {
    sum += ADC_Read( channel );
  }

  return (uint16_t)( sum / nsamples );
}

/*
static int32_t getADC( void )
{
    ADCSRA  |=_BV(ADSC);            // start conversion
    while( (ADCSRA & _BV(ADSC)) );    // wait until conversion is finished

    return ADC;
}
*/

// global storage
extern int16_t lightVal;


/*
 * smooth Value
 */
int smooth(int data, float filterVal, float smoothedVal){

  if (filterVal > 1){      // check to make sure params are within range
    filterVal = .99;
  }
  else if (filterVal <= 0){
    filterVal = 0;
  }

  smoothedVal = (data * (1 - filterVal)) + (smoothedVal  *  filterVal);

  return (int)smoothedVal;
}
/*
 * get measurements
 */
int16_t getBrightness( uint8_t iter )
{
    ADC_Init();
    //int16_t raw_value = ADC_Read_Avg( 1, iter );
    int16_t lightVal = ADC_Read(0);
    //lightVal = smooth(raw_value, LPF_FACTOR, lightVal);
    return lightVal;
}


