#include <Arduino_RouterBridge.h>

const int relayPin = 4;

void setup()
{
    pinMode(relayPin, OUTPUT);

    // Fan OFF initially
    digitalWrite(relayPin, LOW);

    Bridge.begin();

    // Function callable from Python
    Bridge.provide("set_led_state", set_led_state);
}

void loop()
{
    // Nothing here
}

// Called from Python when Ganesh is detected
void set_led_state(bool state)
{
    if (state)
    {
        // Turn fan ON
        digitalWrite(relayPin, LOW);

        // Keep it ON for 5 seconds
        delay(5000);

        // Turn fan OFF
        digitalWrite(relayPin, HIGH);
    }
}
