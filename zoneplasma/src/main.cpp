#include <OctoWS2811.h>
//#include <FastLED.h>

#include "plasma.h"
#include "FastLED.h"

#define PENROSE_ARM 2
#include "zonemap.h"

#define COLS_LEDs 120  // all of the following params need to be adjusted for screen size
#define ROWS_LEDs 8  // LED_LAYOUT assumed 0 if ROWS_LEDs > 8
#define LEDS_PER_STRIP (COLS_LEDs * (ROWS_LEDs / 8))

DMAMEM int displayMemory[LEDS_PER_STRIP*6];
int drawingMemory[LEDS_PER_STRIP*6];
const int config = WS2811_GRB | WS2811_800kHz;
OctoWS2811 leds(LEDS_PER_STRIP, displayMemory, drawingMemory, config);

//def lerp(a, b, t):
//    return a + t * (b - a)

void setup()
{
  pinMode(13, OUTPUT);
  leds.begin();
  leds.show();
}

void loop()
{
  unsigned long frameCount=25500;  // arbitrary seed to calculate the three time displacement variables t,t2,t3
  while(1) {

    for (uint8_t y = 0; y < ROWS_LEDs; y++) {
      for (uint8_t x = 0; x < COLS_LEDs ; x++) {
        //int color = plasma_rgb(frameCount, x, y);

        uint8_t p = plasma(frameCount, x, y);

        uint8_t d = abs(p - 128);
        uint8_t s = lerp8by8(0, 255, p);
        uint8_t l = lerp8by8(0.8 * 255, 255, p);

        uint8_t smix = lerp8by8(255, 179, d);
        uint8_t lmix = lerp8by8(255, 101, d);

        uint16_t index = y * COLS_LEDs + x;

        CRGB color(0);

        switch(zonemap[index]) {
          case ZONE_A1:
          case ZONE_A2:
            color.setHSV(0, s, l);
            break;
          case ZONE_AB1:
          case ZONE_AB2:
            color.setHSV(lerp8by8(0, 0.4 * 255, p), smix, lmix);
            break;
          case ZONE_B1:
          case ZONE_B2:
            color.setHSV(0.4 * 255, s, l);
            break;
          case ZONE_BC1:
          case ZONE_BC2:
            color.setHSV(lerp8by8(0.4 * 255, 0.8 * 255, p), smix, lmix);
            break;
          case ZONE_C1:
          case ZONE_C2:
            color.setHSV(0.7 * 255, s, l);
            break;
          case ZONE_AC1:
          case ZONE_AC2:
            color.setHSV(lerp8by8(0.7 * 255, 1.0 * 255, p), smix, lmix);
            break;
          default:
          case ZONE_off:
            break;
        }

        // channel debugging
        //color.setHSV(y * 30, 255, 255);

        leds.setPixel(index, color.r << 16 | color.g << 8 | color.b);
      }
    }
    frameCount++;

    digitalWrite(13, HIGH);
    leds.show();  // not sure if this function is needed  to update each frame
    digitalWrite(13, LOW);
  }
}
