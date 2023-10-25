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
        Direction getDirection();
        virtual unsigned short getRaw();
};

class WiredRaven : public Raven {
    public:
        WiredRaven(Motorsteuerung* steuerung);
        Direction getDirection();
        unsigned short getRaw();
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
