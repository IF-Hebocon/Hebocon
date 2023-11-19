/*
#include <nRF24L01.h>
#include <RF24.h>


#define CE_PIN  9
#define CSN_PIN 10

#define ADDRESS 42

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

  radio.begin();
  radio.setAutoAck(false);
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_250KBPS);
  radio.setPayloadSize(sizeof(unsigned short));
  radio.openWritingPipe(address);

  Serial.println(radio.isChipConnected());
}

void loop() {
  while (!read()) delay(10);
  
  Serial.println(direction);
  radio.write(&direction, sizeof(direction));
  delay(100);
}

bool read() {
  if (Serial.available() < 2) return false;
  Serial.readBytes((char*)&direction, sizeof(direction));
  return true;
}

void send() {
  radio.write(&direction, sizeof(direction));
}
*/

#include <RF24.h>

RF24 radio(9, 10); // CE, CSN

const byte address[6] = { 0x13, 0x37, 0x69, 0x42, 0xDE };

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.stopListening();
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.setPayloadSize(sizeof(unsigned short));
  radio.openWritingPipe(address);
}

void loop() {
  const unsigned short data = 420;
  Serial.println(radio.write(&data, sizeof(data)));
  delay(100);
}

