#include <Motorsteuerung.h>
#include <Raven.h>

#define CE_PIN 9
#define CSN_PIN 10

const WirelessRaven raven(CE_PIN, CSN_PIN);
const Motorsteuerung motorsteuerung(5, 4, 3, 2);

void setup() {
}

void loop() {
  motorsteuerung.drive(raven.getDirection());
}