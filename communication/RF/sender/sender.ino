#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


#define CE_PIN 10
#define CSN_PIN 9

const byte slaveAddress[22] = "ah8Bgq2UQja5uv3Ex6hJ6q";

RF24 radio(CE_PIN, CSN_PIN);

enum Direction { FORWARD = 1,
                 LEFT = 2,
                 BACKWARD = 3,
                 RIGHT = 4 };

unsigned short direction;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(.1);

  radio.begin();
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(3, 5);
  radio.openWritingPipe(slaveAddress);
}

void loop() {
  while (!Serial.available());
  if (read()) {
    send();
  }
}

bool read() {
  direction = Serial.readString().toInt();
  return direction != 0;
}

void send() {
  radio.write(&direction, sizeof(direction));
}