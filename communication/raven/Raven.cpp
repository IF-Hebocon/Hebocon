#include "Raven.h"


WirelessRaven::WirelessRaven(byte* address, unsigned short cePin, unsigned short csnPin ) {
    this->radio = new RF24(cePin, csnPin);
    this->radio->begin();
    this->radio->setDataRate(RF24_250KBPS);
    this->radio->openReadingPipe(1, address);
    this->radio->startListening();
}

Direction WirelessRaven::getDirection() {
    while (!this->radio->available());
    unsigned short direction;
    radio.read(&direction, sizeof(direction));
    return static_cast<Direction>(direction);
}