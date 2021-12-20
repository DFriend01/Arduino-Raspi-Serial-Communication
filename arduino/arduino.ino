#include <led_config_handler.h>

#define BUTTON_PIN 2
#define LED_1_PIN 3
#define LED_2_PIN 4
#define LED_3_PIN 5
#define LED_4_PIN 6
#define NUM_LEDS 4

LedConfigHandler_t * handler;

void setup() {
  Serial.begin(9600);
  byte pins[4] = {LED_1_PIN, LED_2_PIN, LED_3_PIN, LED_4_PIN};
  handler = init_LedConfigHandler(pins, NUM_LEDS, BUTTON_PIN);
}

void loop() {
  if(update_leds(handler)) {
    Serial.print(get_led_config(handler));
  }
}
