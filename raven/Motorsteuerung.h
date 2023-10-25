class Motor {
    private:
        unsigned short pinA;
        unsigned short pinB;
    public:
        Motor(unsigned short pinA, unsigned short pinB);
        void forward();
        void backward();
        void stop();
};

enum Direction { FORWARD = 1,
                 LEFT = 2,
                 BACKWARD = 3,
                 RIGHT = 4,
                 STOP = 5 };

class Motorsteuerung {
    private:
        Motor* left;
        Motor* right;
    public:
        Motorsteuerung(unsigned short pinLeft1, unsigned short pinLeft2,
                       unsigned short pinRight1, unsigned short pinRight2);
        void drive(Direction direction);
};

