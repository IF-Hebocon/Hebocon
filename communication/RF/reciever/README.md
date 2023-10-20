# Reciever
<ins>__Falls ein RF-Nano verwendet wird, sind die Werte CE_PIN und CSN_PIN eventuell vertauscht!__</ins>

Damit der Reciever Arduino Daten von einem anderen Arduino empfangen kann muss die Konstante `address` auf beiden Arduinos übereinstimmen.

# Fortbewegung
Für die Fortbewegung wird in der Methode `drive` ein switch case über die verschiedenen eingaben gelegt. In den jeweiligen cases kann dann der Roboter fortbewegt werden. Hierzu sollte eine Motorsteuerung eingebaut werden. Der aufbau der Motorsteuerung wird in der [Readme des Hauptprojekts](../../../README.md) beschrieben