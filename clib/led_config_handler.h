#ifndef _LED_CONFIG_HANDLER_H_
#define _LED_CONFIG_HANDLER_H_

#define MAX_LEDS 8

#include <Arduino.h>

/**
 * @typedef  LedConfigHandler_t
 * 
 * @brief
 * 
 *    Handles the LED configuration by reading digital inputs and
 *    updating the configuration after an interrupt event triggered 
 *    by a pushbutton.
 * 
 * @field    pinouts        An array mapping LEDs to digital pin numbers on the 
 *                          Arduino. The maximum number of digital pins to be mapped
 *                          is 8.
 * 
 * @field    button_pinout  The digital pin number that corresponds to the
 *                          interrupt pin that triggers the LED configuration to
 *                          be updated.
 * 
 * @field    led_config     A byte representing the current LED configuration where
 *                          each bit indicates if an LED is on or not (0 - off, 1 - on).
 * 
 * @field    size           The number of LEDs being mapped. The maximum size is 8.
 * 
 */
typedef struct LedConfigHandler {
    byte pinouts[MAX_LEDS];
    byte button_pinout;
    byte led_config;
    unsigned size;
} LedConfigHandler_t;

// Allows C functions to be called by C++
#ifdef __cplusplus
extern "C" {
#endif

/**
 * @function    init_LedConfigHandler
 * 
 * @brief 
 * 
 *    Initializes an LedConfigHandler struct and sets up the pin modes
 *    for each pin and the interrupt handler for the pushbutton.
 * 
 * @param pinMappings   An array containing digital pin numbers for each LED.
 * 
 * @param length        The length of the pinMappings array.
 * 
 * @param buttonPin     The digital pin number for the pushbutton.
 * 
 * @return LedConfigHandler_t*
 * 
 *    Returns a pointer to the handler.
 */
LedConfigHandler_t * init_LedConfigHandler(byte pinMappings[], unsigned length, byte buttonPin);

/**
 * @function get_led_config
 * 
 * @brief 
 * 
 *    Get the current LED configuration from the handler object.
 * 
 * @param handler   A pointer to a LedConfigHandler_t object.
 * 
 * @return byte 
 * 
 *    Returns a byte representing the current LED configuration where each
 *    bit corresponds to the status of each LED (0 - off or 1 - on).
 */
byte get_led_config(LedConfigHandler_t * handler);

/**
 * @function update_leds
 * 
 * @brief 
 * 
 *    Updates the LED configuration according to the digital inputs read from the
 *    Arduino. The LED configuration will only updated when the pushbutton is pushed.
 *    Otherwise, it remains the same.
 * 
 * @param handler   A pointer to a LedConfigHandler_t object.
 * 
 * @return bool
 * 
 *    Returns true if the LED configuration was successfully updated as a result of
 *    the push button being pressed. Otherwise, false is returned indicating that the
 *    LED configuration was not updated.
 *  
 */
bool update_leds(LedConfigHandler_t * handler);

// Allows C functions to be called by C++
#ifdef __cplusplus
}
#endif

#endif //_LED_CONFIG_HANDLER_H_
