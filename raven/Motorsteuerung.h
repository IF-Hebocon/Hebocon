typedef unsigned char byte;

enum Direction : byte;
class Motorsteuerung;
class Motor;

enum Direction : byte {
    FORWARD = 1,
    LEFT = 2,
    BACKWARD = 3,
    RIGHT = 4,
    STOP = 5 
};

class Motorsteuerung {
    private:
        Motor* left;
        Motor* right;
    public:
        Motorsteuerung(byte pinLeft1, byte pinLeft2,
                       byte pinRight1, byte pinRight2);
        void drive(Direction direction);
};

class Motor {
    private:
        byte pinA;
        byte pinB;
    public:
        Motor(byte pinA, byte pinB);
        void forward();
        void backward();
        void stop();
};