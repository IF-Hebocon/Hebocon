# Hebocon

Herzlich Willkommen zum HOKO Weeks InterFace Hebocon Event.

Ein Hebocon ist ein Roboterkampf. Wer jetzt allerdings an ein Duell futuristischer und bis an die Zähne bewaffneter
Maschinen denkt, wird leider enttäuscht. Denn das Wort ”heboi” stammt aus dem Japanischen und bedeutet so viel wie
“minderwertig” oder “peinlich”. Und genau das macht einen Hebocon auch aus. Ein Konstrukt zählt als Hebocon, wenn es
sich bewegt (mechanisch oder elektrisch), nicht größer als 50 x 50 cm ist und nicht mehr als ein Kilogramm wiegt.

Aus zur Verfügung gestellten Schrott-Teilen z.B. Ränder, Platinen, Sensoren, Metallplatten etc. werden Roboter gebaut,
die auf Basis einer Code-Basis gesteuert werden. Gebastelt wird an beiden Workshop-Tagen.

Highlight ist das Turnier am zweiten Tag (ab 14:30 Uhr) mit Siegerehrung und Preisverleihung.

## Anleitung

In dieser Anleitung erfährst du mehr darüber wie du deinen Roboter Bauen und Programmieren kannst. Der großteil der
Programmierarbeit ist schon getan, du musst lediglich eine kommunikationsart wählen und eventuell das Beispielprogramm 
anpassen.

## Motorsteuerung

Die Roboter fahren mithilfe einer Motorsteuerung. Diese Motorsteuerung kann ebenfalls mithilfe des so eben
angesprochenen Programms gesteuert werden. Das bedeutet du musst lediglich die Motorsteuerung wie in dem Bild
dargestellt anschließen.

<div style="display: flex; flex-direction: row">
    <img src="schaltungen/L9110S schaltung.png" alt="Schaltung" height="60%" width="60%"/>
    <img src="schaltungen/L9110S pinout.png" alt="Schaltung" height="40%" width="40%"/>
</div>

## Kommunikation

Du kannst zwischen zwei Kommunikationsarten wählen

### Kabellos

Für die kabellose Kommunikation wird ein RF Chip verwendet. In folgender Schaltung wird gezeigt wie man diesen
anschließt.

<div style="display: flex; flex-direction: row">
    <img src="schaltungen/nRF24l01 schaltung.png" alt="Schaltung" height="60%" width="60%"/>
    <img src="schaltungen/nRF24l01 pinout.png" alt="Schaltung" height="40%" width="40%"/>
</div>

### Kabelgebunden

Für die kabelgebundene Kommunikation wird lediglich ein USB-Kabel benötigt.
