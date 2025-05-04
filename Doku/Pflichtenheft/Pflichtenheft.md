---
title: STECH-Softwareprojekt Dokumentation
author: Felix Jäckel, Sebastian Schöneich, Eric Malik Uecker, Benjamin Waschkowski, Paul Weibbrecht
date: 04-05-2025
version: 1.1
---
# STECH-Projektarbeit - Pflichtenheft
Bearbeiter: Felix Jäckel, Sebastian Schöneich, Eric Malik Uecker, Benjamin Waschkowski, Paul Weibbrecht
Seminargruppe: 3MI23-1

## Miroboard
Als Grundlage für das Pflichtenheft stehen die Screenshots unseres Miroboards (zu finden im Ordner /Doku/Miro/).
Innerhalb dieses Dokuments werden einzelne Punkte korrigiert, gestrichen und/oder hinzugefügt.

### Miro_KickOff
- Chat: Verworfen
- Läuft auf Root-Server: Teils Verworfen (möglicherweise in der Präsentation verwirklicht)

daraus resultiert:
* Komponenten:
> Frontend, Backend, Verbindung-Frontend-Backend, P2P-Funktionabilität

* Frontend:
> Login-Seite\
> Startseite\
> Spielseite

* Backend:
> Python\
> Login Verifizierung\
> Datenbank\
> Gamelogik

### Miro_BackEnd
- Timer: wurde aus den Anforderungen für Version 1 entfernt
- SignUp - Passwort-Mindestlänge: wurde aus den Anforderungen für Version 1 entfernt

daraus resultiert:
* Gamelogik:
> Spielbrett Darstellung als 2D-Array\
> Jede Figur an Stelle im Array\
> Erlaubte Spielzüge für jede Spielfigur, mit Überprüfung ob Erlaubt, Schlag, Schach oder Schachmatt\
> Spielfiguren als Objekte

* SignUp:
> Credentials: Nutzername, Passwort\
> Fehler wenn Nutzername bereits vergeben

* Login:
> Verifikation mit Credentials

* Datenbank:
> Mittels SQLite\
> DB 1 - USER: ID, user_name, hashed_password\
> DB 2 - GameHistory: ID, user1, user2, winner

* Objekt-Spielfigur:
> Attribute - Besitzer, Farbe, Position, Spielzüge\
> Methoden - Möglichkeiten zur Umsetzung des weiter oben beschriebenen