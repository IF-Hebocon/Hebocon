#include "Motorsteuerung.h"
#include <Arduino.h>

Motor::Motor(unsigned short pinA, unsigned short pinB) {
    this->pinA = pinA;
    this->pinB = pinB;
    pinMode(pinA, OUTPUT);
    pinMode(pinB, OUTPUT);
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
}

void Motor::forward() {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, LOW);
}

void Motor::backward() {
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, HIGH);
}

void Motor::stop() {
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
}


Motorsteuerung::Motorsteuerung(unsigned short pinLeft1, unsigned short pinLeft2,
                               unsigned short pinRight1, unsigned short pinRight2) {
    this->left = new Motor(pinLeft1, pinLeft2);
    this->right = new Motor(pinRight1, pinRight2);
}

Motorsteuerung::drive(Direction direction) {
    switch (direction) {
    case FORWARD:
        this->left->forward();
        this->right->forward();
        break;
    case BACKWARD:
        this->left->backward();
        this->right->backward();
        break;
    case LEFT:
        this->left->backward();
        this->right->forward();
        break;
    case RIGHT:
        this->left->forward();
        this->right->backward();
        break;
    default:
        this->left->stop();
        this->right->stop();
        break;
    }
}
