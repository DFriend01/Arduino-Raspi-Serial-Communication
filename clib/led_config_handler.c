#include "led_config_handler.h"

static void set_pinmodes(LedConfigHandler_t *);
static void setup_pushbutton_interrupt(LedConfigHandler_t *);
static byte read_led_config(LedConfigHandler_t *);
static bool should_update_leds(void);
static void interrupt_handler(void);

static volatile bool update_led_config = false;

LedConfigHandler_t * init_LedConfigHandler(byte pinMappings[], unsigned length, byte buttonPin) {
    LedConfigHandler_t * handler = malloc(sizeof(LedConfigHandler_t));

    handler->size = (length > MAX_LEDS) ? MAX_LEDS : length;

    for(unsigned i = 0; i < MAX_LEDS; i++) {
        handler->pinouts[i] = pinMappings[i];
    }

    handler->button_pinout = buttonPin;
    handler->led_config = 0;

    set_pinmodes(handler);
    setup_pushbutton_interrupt(handler);

    return handler;
}

byte get_led_config(LedConfigHandler_t * handler) {
    return handler->led_config;
}

bool update_leds(LedConfigHandler_t * handler) {
    if(should_update_leds()) {
        noInterrupts();
        byte led_config = read_led_config(handler);
        handler->led_config = led_config;
        update_led_config = false;
        interrupts();
        return true;
    }
    return false;
}

static void set_pinmodes(LedConfigHandler_t * handler) {
    for(unsigned i = 0; i < handler->size; i++) {
        pinMode(handler->pinouts[i], INPUT_PULLUP);
    }
}

static void setup_pushbutton_interrupt(LedConfigHandler_t * handler) {
    pinMode(handler->button_pinout, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(handler->button_pinout), interrupt_handler, RISING);
}

static byte read_led_config(LedConfigHandler_t * handler) {
    byte sequence = 0;

    for(unsigned i = 0; i < handler->size; i++) {
        sequence |= (digitalRead(handler->pinouts[i]) << i);
    }

    return sequence;
}

static bool should_update_leds() {
    bool should_update = update_led_config;
    return should_update;
}

static void interrupt_handler() {
    update_led_config = true;
}
