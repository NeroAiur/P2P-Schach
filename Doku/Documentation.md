---
title: STECH-Softwareprojekt Dokumentation
author: Felix Jäckel, Sebastian Schöneich, Eric Malik Uecker, Benjamin Waschkowski, Paul Weibbrecht
date: 04-05-2025
version: 1.1
---
# STECH-Projektarbeit
Bearbeiter: Felix Jäckel, Sebastian Schöneich, Eric Malik Uecker, Benjamin Waschkowski, Paul Weibbrecht
Seminargruppe: 3MI23-1

## Benutze Libraries:
* Django
* sqlite3
* \_\_future\_\_
* copy
* io
* sys
* os
* json
* hashlib

# Backend
* /backend/

## 2darray.py
- Simple Testdatei für das 2-dimensionale Array, zu Verständnis innerhalb der Entwicklung des Softwareprojektes

## ChessTranscode.py
Modul, welches die Übersetzung vom 2D-Array in Schach-Sprache und anders herum verwirklicht

## database_ops.py
Modul, welches jegliche Interaktion des Softwareprojektes mit der Datenbank ermöglicht.\
Darunter fällt:
* Verbindung zur Datenbank
* Validierung der Logindaten
* Anlegen eines Benutzers
* Aktualisierung der Elo-Bewertung des Nutzers

## Game.py
Quasi das "main"-Modul des Backends. Berechnet alle möglichen Bewegungen der Spielfiguren und gleicht ab ob die, vom Backend erhaltenen Informationen valide sind.
Trifft dies zu, wird die Bewegung und eventuelle Schläge etc durchgeführt und der neue GameState ans Frontend übertragen, damit dies es visualisieren kann.

## Move.py
Gerüst-Modul für die Bewegungen der einzlenen Spielfiguren

## Pieces.py
Modul, welches jegliche Informationen zu allen Arten von Spielfiguren, als Klasse mit entsprechenden Attributen beinhält.\
Hierüber werden jegliche Figuren im Spiel initialisiert.

# Frontend
* /django/chess_app/static/Chesspieces/SVG/ (SVG-Dateien)
* /django/chess_app/static/css/ (CSS-Dateien)
* /django/chess_app/static/css/fonts/ (Schriftarten)
* /django/chess_app/static/js/ (JavaScript-Dateien)
* /django/chess_app/templates/ (HTML-Dateien)

## CSS
styles.css beinhält jegliche Styles, die auf den Webseiten des Projektes benutzt wurden.

## HTML

### base.html
Testdatei

### chessboard.html
HTML-Datei, welche die Website beschreibt, die bei einem laufenden Schach-Spiel angezeigt wird

### dashboard.html
HTML-Datei, welche die Website beschreibt, die als Landing-Page für einen angemeldeten Nutzen benutzt wird.\
Über diese kann u.A. ein neues Spiel gestartet werden.

### index.html
HTML-Datei, welche die Website beschreibt, die als Landing-Page für einen nicht angemeldeten Nutzen benutzt wird.\
Über diese Seite kann sich angemeldet oder registriert werden.

## JS

### chessboard.js
Frontend eines laufenden Schachspiels.\

|Funktion | Erklärung |
|---------|-----------|
| awaitGame() | stellt regelmäßig eine Anfrage ob ein zweiter Spieler vorhanden ist |
| requestGameState() | wird regelmäßig aufgerufen, vergleicht lokalen (sichtbaren) Spielstand mit tatsächlichem (im Backend) und aktualisiert diesen über updateGameState() |
| updateGameState(JSON) | wird von anderen Funtkionen aufgerufen. Blockiert Interaktionen, Dekodiert Spieldaten, Aktiviert Interaktionen für nächsten Zug |
| decodeMoves() | Dekodiert alle möglichen Züge einer Spielfigur und listet diese in einem Array auf |
| setUpGame() | Startgeneration des Spielbrettes |

### dashboard.js
Frontend für Lobby-Browser, Ranglisten-Board und Freundesliste

|Funktion | Erklärung |
|---------|-----------|
| fetchLobbys() | fragt alle vorhandenen Lobbies an und packt sie in eine Liste, anklickbar um diese beizutreten |
| fetchRanking() | fragt die Ranglistenwertung an und stellt sie dar - WIP |
| fetchFriends() | fragt die Freundestliste an und stellt sie dar - WIP |

### helperScript.js
Diverse Helper-Skripte

|Funktion | Erklärung |
|---------|-----------|
| setAttributes(el, attrs) | wendet css styles (attrs) in Form von JSON auf elemente (el) an |
| setUpHTML(type, attributes, parent) | Erstellt und fügt ein neues HTML-Element hinzu |
| setUpSVG(type, attributes, parent) | Erstellt und fügt ein neues SVG-Element hinzu |
| hash(input) | hasht den input und gibt ihn zurück |
| getCookie(name) | fragt den Wert des cookies mit dem Namen "name" an |

### loginForm.js
Skripte, die bei der Bearbeitung des Login/Registrations-Prozesses verwendet werden.

|Funktion | Erklärung |
|---------|-----------|
| fetchLogin() | nimmt eingetragene Daten und sendet sie als Login-Versuch in einer form ab |
| fetchSignUp() | nimmt eingetragene Daten und sendet sie als Registrations-Versuch in einer form ab |

### pieces.js
Skripte zur Bearbeitung der Interaktionen mit den Spielfiguren

|Funktion | Erklärung |
|---------|-----------|
| remove() | entfernt Spielfigur |
| startListen() | macht Spielfiguren interaktiv, wenn man am Zug ist |
| stopListen() | Entfernt Interaktivität der Spielfiguren |
| startDrag() | zeigt alle möglichen Spielzüge an und hängt die Spielfigur an den Mauszeiger dran |
| dragPiece(event) | Funktion für die laufende Bewegung der SVG mit dem Mauszeiger |
| endDrag() | Entscheidet ob der "abgesetzte" Punkt einen validen Spielzug darstellt und schickt, falls dem so ist, diesen Spielzug ans Backend zur weiteren Bearbeitung |
