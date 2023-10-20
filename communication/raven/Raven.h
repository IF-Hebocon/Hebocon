#include "Motorsteuerung.h"
#include <RF24.h>

using byte = unsigned char;

class Raven {
    public:
        virtual Direction getDirection();
};

class WirelessRaven : public Raven {
    private:
        RF24* radio;
    public:
        WirelessRaven(byte* address, unsigned short cePin, unsigned short csPin);
};