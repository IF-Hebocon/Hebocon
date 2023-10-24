#include "Raven.h"


Raven::Raven(Motorsteuerung* steuerung) {
    Serial.begin(9600);
    this->steuerung = steuerung;
}

void Raven::loop() {
    if (!this->steuerung) return;
    const Direction direction = this->getDirection();
    this->steuerung->drive(direction);
}


WiredRaven::WiredRaven(Motorsteuerung* steuerung) : Raven(steuerung) {

}

unsigned short WiredRaven::getRaw() {
    while (Serial.available() <= 1) { delay(10); Serial.println(Serial.available()); };
    unsigned short data;
    Serial.readBytes((char*)&data, sizeof(data));
    return data;
}

Direction WiredRaven::getDirection() {
    return static_cast<Direction>(this->getRaw());
}



WirelessRaven::WirelessRaven(Motorsteuerung* steuerung, unsigned short wirelessNumber) : WirelessRaven(steuerung, wirelessNumber, 9, 10) {

}

WirelessRaven::WirelessRaven(Motorsteuerung* steuerung, unsigned short wirelessNumber, unsigned short cePin, unsigned short csnPin) : Raven(steuerung) {
    uint8_t address[6];
    sprintf(address, "WAN%02u", wirelessNumber);

    this->radio = new RF24(cePin, csnPin);

    Serial.print("Chip connected: ");
    Serial.println(this->radio->isChipConnected());
    Serial.print("Chip begin: ");
    Serial.println(this->radio->begin());

    this->radio->setAutoAck(false);
    this->radio->setPALevel(RF24_PA_MAX);
    this->radio->setDataRate(RF24_250KBPS);
    this->radio->setPayloadSize(sizeof(unsigned long));
    this->radio->openReadingPipe(1, address);
    this->radio->startListening();

    Serial.println("Ready");
}

unsigned short WirelessRaven::getRaw() {
    while (!this->radio->available()) delay(10);
    unsigned short direction;
    this->radio->read(&direction, sizeof(direction));
    return direction;
}

Direction WirelessRaven::getDirection() {
    return static_cast<Direction>(this->getRaw());
}