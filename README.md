# qLearning
Leichte Django-Lernplattform zum Erstellen und Wiederholen eigener Karteikarten.

## Funktionen
- Benutzerkonten mit Registrierung, Login und persönlichem Kartenbestand
- Dashboard mit Anzahl fälliger Karten sowie Kategorienübersicht
- Karten einzeln anlegen oder gebündelt per CSV importieren (Delimiter wird automatisch erkannt)
- Optionales Kartenbild mit einfachem Viewer (Rotieren/Zoom/Thumbnail) und serverseitiger Bildaufbereitung (Pillow)
- Lernmodus pro Kategorie: Frage zeigen, Antwort aufdecken, nächste fällige Karte ziehen
- CSV-Import vermeidet Duplikate und akzeptiert optionale Kategorie-Spalte

## Voraussetzungen
- Python 3.11+
- Virtualenv oder ein anderes Werkzeug zum Isolieren der Umgebung

## Projekt starten
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser    # oder im UI registrieren
python manage.py runserver
```
Das Projekt läuft danach unter <http://127.0.0.1:8000>. Medien werden im Verzeichnis `cards_images/` gespeichert (siehe `MEDIA_ROOT` in `spanisch_trainer/settings.py`).

## Karten hinzufügen
- **Einzelerfassung:** Formular unter `/add/` mit Frage, Antwort, Kategorie und optionalem Bild ausfüllen.
- **CSV-Import:** UTF‑8 Datei ohne Kopfzeile mit `question,answer[,category]`. Der Import informiert über neue, übersprungene oder fehlerhafte Zeilen.

## Bilder & Viewer
Im Lernmodus erscheint das gespeicherte Bild einer Karte. Über die Buttons unter dem Bild lassen sich Rotation, Zoomstufe und eine generierte Vorschau steuern. Serverseitig übernimmt `flashcards/utils/image_utils.py` das Zuschneiden, Skalieren und Orientieren der Datei.

## Roadmap / Ideen
1. Karten in der Oberfläche löschen oder archivieren können
2. UI/UX verfeinern (Buttons, Responsiveness, Dark Mode)
3. Leitner-Intervalle nach einer Antwort aktualisieren und Statistiken visualisieren
