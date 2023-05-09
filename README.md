# Conways Spiel des Lebens - Kiste Edition

Conways Spiel des Lebens ist ein von dem Mathematiker **John Conway** im Jahr 1970 erfundener zellulärer Automat. Es ist ein **Null-Spieler-Spiel**, was bedeutet, dass seine Entwicklung durch seinen Anfangszustand bestimmt wird und keine weitere Eingabe erfordert. Das Spiel ist ein klassisches Beispiel für **Emergenz**, bei der komplexe Muster aus einfachen Regeln entstehen.

Diese Implementierung des Spiels verwendet die Bibliotheken **Pygame** und **Numpy** zur Erstellung der Simulation und die Bibliothek **PyQt6** zur Erstellung der Benutzeroberfläche. Das Spielbrett ist ein **100x100 Raster**, in dem jede Zelle entweder lebendig oder tot sein kann. Das Spiel beginnt mit einer zufälligen Konfiguration von Zellen und der Benutzer kann mit dem Brett interagieren, indem er auf die Zellen klickt, um ihren Zustand umzuschalten oder die Leertaste verwendet, um die Simulation zu starten/anhalten.

![Gosper's Glider Gun](https://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif)