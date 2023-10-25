#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


#define CE_PIN  9
#define CSN_PIN 10

#define ADDRESS 420

RF24 radio(CE_PIN, CSN_PIN);

enum Direction { FORWARD = 1,
                 LEFT = 2,
                 BACKWARD = 3,
                 RIGHT = 4,
                 STOP = 5 };

unsigned short direction;

void setup() {
  uint8_t address[6];
  sprintf(address, "WAN%02u", ADDRESS);

  Serial.begin(9600);
  Serial.setTimeout(.1);

  radio.begin();
  radio.setRetries(3, 5);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.setPayloadSize(sizeof(unsigned long));
  radio.openWritingPipe(address);
}

void loop() {
  if (!Serial.available()) return;
  if (read()) {
    send();
  }
}

bool read() {
  Serial.readBytes((char*)&direction, sizeof(direction));
  return direction != 0;
}

void send() {
  radio.write(&direction, sizeof(direction));
}
