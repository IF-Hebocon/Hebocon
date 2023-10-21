#include "Motorsteuerung.h"
#include <RF24.h>
#include <Arduino.h>

using byte = unsigned char;

class Raven {
    private:
        Motorsteuerung* steuerung;
    public:
        Raven(Motorsteuerung* steuerung);
        void loop();
        virtual Direction getDirection() = 0;
        virtual unsigned short getRaw() = 0;
};

class WiredRaven : public Raven {
    public:
        WiredRaven(Motorsteuerung* steuerung);
        Direction getDirection() override;
        unsigned short getRaw() override;
};

class WirelessRaven : public Raven {
    private:
        RF24* radio;
    public:
        WirelessRaven(Motorsteuerung* steuerung, unsigned short wirelessNumber);
        WirelessRaven(Motorsteuerung* steuerung, unsigned short wirelessNumber, unsigned short cePin, unsigned short csPin);
        Direction getDirection() override;
        unsigned short getRaw() override;
};