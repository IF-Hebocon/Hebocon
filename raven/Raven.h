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
        virtual byte getRaw() = 0;
};

class WiredRaven : public Raven {
    public:
        WiredRaven(Motorsteuerung* steuerung);
        byte getRaw() override;
};

class WirelessRaven : public Raven {
    private:
        RF24* radio;
    public:
        WirelessRaven(Motorsteuerung* steuerung, byte wirelessNumber);
        WirelessRaven(Motorsteuerung* steuerung, byte wirelessNumber, byte cePin, byte csPin);
        byte getRaw() override;
};
