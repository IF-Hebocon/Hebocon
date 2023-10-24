#include <Raven.h>
#include <Motorsteuerung.h>

#define MOTOR_A1 2
#define MOTOR_A2 3
#define MOTOR_B1 4
#define MOTOR_B2 5

#define CE_PIN 9
#define CSN_PIN 10

#define ADDRESS 420

Raven* raven;

void setup() {
    const Motorsteuerung* steuerung = new Motorsteuerung(MOTOR_A1, MOTOR_A2, MOTOR_B1, MOTOR_B2);
    raven = new WirelessRaven(steuerung, ADDRESS, CE_PIN, CSN_PIN);
}

void loop() {
    raven->loop();
}
