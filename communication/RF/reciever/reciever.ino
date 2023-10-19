#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


#define CE_PIN 9
#define CSN_PIN 10

const byte address[22] = "ah8Bgq2UQja5uv3Ex6hJ6q";

RF24 radio(CE_PIN, CSN_PIN);

enum Direction { FORWARD = 1,
                 LEFT = 2,
                 BACKWARD = 3,
                 RIGHT = 4 };

unsigned short direction;
bool newData = false;

void setup() {
  radio.begin();
  radio.setDataRate(RF24_250KBPS);
  radio.openReadingPipe(1, address);
  radio.startListening();

  pinMode(4, OUTPUT);
}

void loop() {
  getData();
  showData();
}

void getData() {
  if (radio.available()) {
    radio.read(&direction, sizeof(direction));
    newData = true;
  }
}

void showData() {
  if (newData == true) {
    newData = false;
    drive();
  }
}

void drive() {
  switch (direction) {
    case FORWARD:
      digitalWrite(4, LOW);
      break;
    case LEFT:
      digitalWrite(4, HIGH);
      break;
    case BACKWARD:
      digitalWrite(4, LOW);
      break;
    case RIGHT:
      digitalWrite(4, HIGH);
      break;
    default:
      break;
  }
}
