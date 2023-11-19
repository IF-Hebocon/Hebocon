#include <nRF24L01.h>
#include <RF24.h>


#define CE_PIN  9
#define CSN_PIN 10

typedef unsigned char byte;

#define ADDRESS_FLAG 137
#define CONTROL_FLAG 186

#define ACK true


RF24* radio = NULL;

struct Packet {
  byte flag;
  byte value;
};

void setupRadio(const byte* address) {
  if (radio == NULL) {
    radio = new RF24(CE_PIN, CSN_PIN);
    radio->begin();
    radio->setAutoAck(ACK);
    radio->setPALevel(RF24_PA_LOW);
    radio->setDataRate(RF24_250KBPS);
    radio->setPayloadSize(sizeof(byte));
  }
  radio->openWritingPipe(address);
}

void handleAddress(byte value) {
  byte address[6];
  sprintf(address, "WAN%02u", value);
  setupRadio(address);
  Serial.println("OK");
}

bool read(struct Packet* packet) {
  if (Serial.available() < sizeof(struct Packet)) return false;
  Serial.readBytes((byte*)packet, sizeof(struct Packet));
  return true;
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  struct Packet packet;
  if (!read(&packet)) {
    delay(50);
    return;
  };

  if (packet.flag == ADDRESS_FLAG)
    handleAddress(packet.value);
  else if (packet.flag == CONTROL_FLAG)
    radio->write(&packet.value, sizeof(byte));
}