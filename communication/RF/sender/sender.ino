#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


#define CE_PIN  10
#define CSN_PIN 9

const byte slaveAddress[22] = "ah8Bgq2UQja5uv3Ex6hJ6q";

RF24 radio(CE_PIN, CSN_PIN);

enum Direction { FORWARD, LEFT, BACKWARD, RIGHT };

unsigned short direction;

void setup() {
    Serial.begin(9600);

    radio.begin();
    radio.setDataRate( RF24_250KBPS );
    radio.setRetries(3, 5);
    radio.openWritingPipe(slaveAddress);
}

//====================

void loop() {
    if (Serial.available() && read()) {
        send();
    }
}

bool read() {
  direction = Serial.parseInt();
  return direction != 0;
}

void send() {
    bool rslt;
  
    rslt = radio.write( &direction, sizeof(direction) );

    Serial.print("Data Sent ");
    Serial.print(direction);
    if (rslt) {
        Serial.println("  Acknowledge received");
    }
    else {
        Serial.println("  Tx failed");
    }
}

//================