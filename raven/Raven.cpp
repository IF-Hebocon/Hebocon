#include "Raven.h"


Raven::Raven(Motorsteuerung* steuerung) {
    this->steuerung = steuerung;
}

void Raven::loop() {
    if (!this->steuerung) return;
    const byte data = this->getRaw();
    if (!data) return;
    const Direction direction = static_cast<Direction>(data);
    this->steuerung->drive(direction);
}


WiredRaven::WiredRaven(Motorsteuerung* steuerung) : Raven(steuerung) {
    Serial.begin(9600);
}

byte WiredRaven::getRaw() {
    if (!Serial.available()) return 0;
    byte data;
    Serial.readBytes(&data, sizeof(data));
    return data;
}

WirelessRaven::WirelessRaven(Motorsteuerung* steuerung, byte wirelessNumber) : WirelessRaven(steuerung, wirelessNumber, 9, 10) {

}

WirelessRaven::WirelessRaven(Motorsteuerung* steuerung, byte wirelessNumber, byte cePin, byte csnPin) : Raven(steuerung) {
    uint8_t address[6];
    sprintf(address, "WAN%02u", wirelessNumber);

    this->radio = new RF24(cePin, csnPin);

    this->radio->begin();
    this->radio->setAutoAck(true);
    this->radio->setPALevel(RF24_PA_MAX);
    this->radio->setDataRate(RF24_250KBPS);
    this->radio->setPayloadSize(sizeof(byte));
    this->radio->openReadingPipe(1, address);
    this->radio->startListening();
}

byte WirelessRaven::getRaw() {
    if (this->radio->available() == 0) return 0;
    byte data;
    this->radio->read(&data, sizeof(data));
    return data;
}
