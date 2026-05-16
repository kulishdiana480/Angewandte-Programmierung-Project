# Work Log

**Student Name: Diana Kulish** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?
Am ersten Tag habe ich meine Entwicklungsumgebung vollständig eingerichtet und meine erste FastAPI-Anwendung gebaut. Da Git und VS Code bereits auf meinem Rechner installiert waren, musste ich nur noch uv als neuen Paketmanager installieren, was problemlos funktioniert hat. Ich habe ein neues Projekt initialisiert, FastAPI installiert und die erste main.py Datei erstellt. 
Während der Unterrichtseinheit habe ich gemeinsam mit der Klasse drei Endpunkte gebaut (/, /status, /about) und gelernt, wie FastAPI automatisch eine interaktive Dokumentation unter /docs generiert — was ich zum Testen extrem praktisch fand, da man kein zusätzliches Tool benötigt.

Für die Hausaufgabe habe ich eigenständig drei weitere Endpunkte implementiert:
/square/{number} — berechnet das Quadrat einer Zahl mithilfe von Path-Parametern
/student — gibt meine persönlichen Studenteninformationen zurück
/double/{number} — verdoppelt eine gegebene Zahl

Außerdem habe ich das Konzept von f-Strings für die Berechnungsnachrichten geübt und verstanden, wie FastAPI Path-Parameter automatisch in den richtigen Typ konvertiert (z.B. int).
Verwendete Tools: VS Code, uv, FastAPI, Uvicorn, Browser /docs


---

#### 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

Das Konzept der Dekoratoren wie @app.get("/path") war für mich zunächst neu. Ich habe zwar verstanden, was sie tun, aber die Syntax fühlte sich ungewohnt an — ich war es nicht gewohnt, etwas direkt über eine Funktionsdefinition zu schreiben, um ihr Verhalten zu verändern.
Außerdem habe ich bei einer meiner Hausaufgabenfunktionen zunächst vergessen, einen Wert zurückzugeben, was dazu führte, dass der Endpunkt null statt des erwarteten Ergebnisses zurückgab. Es hat einen Moment gedauert, bis ich das Problem erkannt habe.


---

#### 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

Ich habe die Folie mit dem FastAPI-Muster (@app.get + Funktion + return dict) mehrmals durchgelesen und jeden Endpunkt sofort nach dem Schreiben in /docs getestet. So habe ich das fehlende return schnell entdeckt, da die Antwort offensichtlich falsch war.
Häufiges Testen in /docs nach jeder kleinen Änderung wurde ab Tag 1 zu meiner wichtigsten Strategie.


---

### Day 2

#### 1. ✅ What did I accomplish?

Am zweiten Tag habe ich Python-Grundlagen gelernt (Variablen, Datentypen, Listen, Dictionaries, Funktionen, f-Strings, Type Hints) und diese direkt beim Aufbau einer Notiz-API mit Dateipersistenz angewendet.
Während der Unterrichtseinheit habe ich gemeinsam mit der Klasse folgende Endpunkte gebaut:

POST /notes — erstellt eine neue Notiz und speichert sie in data/notes.json
GET /notes — listet alle Notizen auf, die aus der Datei geladen werden
GET /notes/{note_id} — ruft eine bestimmte Notiz anhand ihrer ID ab, gibt 404 zurück wenn nicht gefunden

Ich habe gelernt, wie Pydantic BaseModel funktioniert — dabei wird NoteCreate (Eingabe ohne ID) und Note (Ausgabe mit ID und Zeitstempel) als zwei separate Modelle definiert, was ein sauberes und professionelles Muster ist.
Für die Hausaufgabe habe ich die API erweitert mit:

Einem category-Feld in beiden Modellen
GET /notes/category/{category} — Notizen nach Kategorie filtern
GET /notes/stats — zeigt die Gesamtanzahl der Notizen und die Anzahl pro Kategorie

Verwendete Tools: VS Code, uv, FastAPI, Pydantic, Python-Module json und pathlib



---

#### 2. 🚧 What challenges did I face?

Die Dateipersistenz war der schwierigste Teil von Tag 2. Ich hatte zunächst eine globale Variable notes_db = [] verwendet und vergessen, load_notes() am Anfang jedes Endpunkts aufzurufen, wodurch die Liste nach einem Serverneustart immer leer war. Es hat eine Weile gedauert, bis ich verstanden habe, warum meine Notizen nach jedem Neustart verschwanden.
Außerdem hatte ich einen Fehler, bei dem ich tags: list[str] = [] direkt als Standardwert im Modell verwendet habe — ich wusste damals noch nicht, dass dies in Python-Klassen zu Problemen mit gemeinsam genutztem veränderbarem Zustand führt.



---

#### 3. 💡 How did I overcome them?

Ich habe die Folie zu den Funktionen load_notes() und save_notes() sorgfältig nochmals gelesen und festgestellt, dass ich load_notes() am Anfang jedes Endpunkts aufrufen muss, der Daten benötigt — und nicht nur einmal beim Start. Nachdem ich das behoben hatte, habe ich den Server gestoppt, neu gestartet und mit GET /notes überprüft, dass die Notizen noch vorhanden waren.
Das Problem mit dem veränderbaren Standardwert habe ich später beim Lesen der Pydantic-Dokumentation entdeckt und in Tag 3 beim Refactoring der Modelle behoben.



---

### Day 3

#### 1. ✅ What did I accomplish?

Tag 3 war der intensivste Tag bisher. Ich habe REST-API-Designprinzipien, den Unterschied zwischen Path- und Query-Parametern gelernt und eine vollständige CRUD-API mit einer echten SQLite-Datenbank implementiert.
Gelernte REST-Prinzipien:

URLs sollten Substantive sein, keine Verben (/notes statt /getNotes)
HTTP-Methoden definieren die Aktion (GET = lesen, POST = erstellen, PUT = aktualisieren, DELETE = löschen)
Query-Parameter dienen zum Filtern, Path-Parameter zur Identifikation

Neu hinzugefügte Endpunkte:

PUT /notes/{note_id} — ersetzt eine Notiz vollständig (alle Felder erforderlich)
PATCH /notes/{note_id} — aktualisiert nur die angegebenen Felder
DELETE /notes/{note_id} — löscht eine Notiz, gibt 204 No Content zurück
GET /notes/stats — Statistiken mit Kategorieanzahl und Top-5-Tags
GET /tags und GET /tags/{tag_name}/notes — Tag-Ressourcen-Endpunkte
GET /categories und GET /categories/{category_name}/notes — Kategorie-Ressourcen-Endpunkte

Datenbankmigration (Hausaufgabe Task 6):
Die größte Leistung von Tag 3 war die Migration vom JSON-Dateispeicher zu einer echten SQLite-Datenbank mit SQLModel. Ich habe drei Datenbanktabellen definiert — notes, tags und notetaglink — um die Many-to-Many-Beziehung zwischen Notizen und Tags zu verwalten. Außerdem habe ich eine Funktion migrate_json_to_database() geschrieben, die beim ersten Start automatisch die vorhandenen Daten aus data/notes.json in die neue Datenbank überträgt.
Zusätzlich habe ich eine datumsbasierte Filterung zu GET /notes mit den Query-Parametern created_after und created_before hinzugefügt.
Verwendete Tools: VS Code, uv, FastAPI, SQLModel, SQLite, SQLite Viewer Extension, Pydantic




---

#### 2. 🚧 What challenges did I face?

Die Many-to-Many-Beziehung zwischen Notizen und Tags war das schwierigste Konzept der gesamten Woche. Zu verstehen, warum eine dritte Tabelle (NoteTagLink) notwendig ist — und wie Relationship() die Modelle verbindet — erforderte erheblichen Aufwand.
Außerdem bin ich beim Implementieren der Tag-Filterung in GET /notes auf einen konkreten Fehler gestoßen. Mein erster Versuch war:
pythonstatement = statement.join(Note.tags).where(Tag.name == tag_lower)
Dies führte zu einem SQLAlchemy-Fehler, da ich die Join-Bedingungen nicht explizit angegeben hatte und die Abfrage nicht wusste, wie sie automatisch über die Verknüpfungstabelle joinen sollte.
Ein weiteres Problem gab es bei der Funktion migrate_json_to_database() — in meinem ersten Versuch hatte ich vergessen zu prüfen, ob die Datenbank bereits befüllt ist, was bei jedem Serverneustart zu doppelten Einträgen führte.



---

#### 3. 💡 How did I overcome them?

Für die Many-to-Many-Beziehung habe ich die SQLModel-Dokumentation zu Relationships gelesen und das Beispiel sorgfältig studiert. Es hat mir sehr geholfen, die drei Tabellen auf Papier zu zeichnen und mit Beispieldaten zu befüllen, um zu verstehen, warum die Verknüpfungstabelle notwendig ist.
Für die Tag-Filter-Abfrage habe ich das Problem behoben, indem ich explizit über die Verknüpfungstabelle gejoint habe:
pythonstatement = (
    statement
    .join(NoteTagLink, Note.id == NoteTagLink.note_id)
    .join(Tag, Tag.id == NoteTagLink.tag_id)
    .where(Tag.name == tag_lower)
)
Beim Migrationsproblem habe ich am Anfang der Funktion migrate_json_to_database() eine Prüfung hinzugefügt, die zuerst die Datenbank abfragt — wenn bereits Notizen vorhanden sind, kehrt die Funktion sofort zurück, ohne etwas zu tun. Dadurch wird sichergestellt, dass die Migration nur einmal ausgeführt wird.
Insgesamt waren häufiges Testen in /docs und sorgfältiges Lesen der Fehlermeldungen die effektivsten Strategien während des gesamten Tag 3.




---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?

Am vierten Tag habe ich das Thema POST-Anfragen und Pydantic-Validierung vertieft und erstmals automatisierte Tests mit pytest geschrieben.
Theorie — POST vs GET:
Ich habe den Unterschied zwischen GET und POST vollständig verstanden. GET liest nur Daten und verändert nichts, während POST neue Ressourcen erstellt und die Daten im Request-Body überträgt. Außerdem habe ich gelernt, warum der Statuscode 201 Created bei erfolgreicher Erstellung korrekter ist als der allgemeine Code 200 OK.
Course API (my-first-api):
Im Unterricht haben wir gemeinsam ein separates Course API gebaut, um das POST-Muster mit Dateipersistenz zu üben. Ich habe die Funktionen load_courses() und save_courses() implementiert, die Daten in einer courses.json Datei speichern. Außerdem habe ich eine Duplikatsprüfung eingebaut — versucht man einen Kurs mit demselben Code erneut zu erstellen, gibt die API den Statuscode 409 Conflict zurück.
Folgende Endpunkte wurden implementiert:

POST /courses — erstellt einen neuen Kurs mit automatisch generierter ID
GET /courses — listet alle Kurse mit optionalen Filtern (semester, min_ects)
GET /courses/{course_id} — gibt einen bestimmten Kurs anhand der ID zurück

Tests mit pytest:
Das Hauptthema des Tages war das Schreiben automatisierter Tests. Ich habe die Bibliotheken pytest und requests installiert und eine vollständige Testdatei test_notes.py erstellt. Alle Tests folgen dem Arrange-Act-Assert-Muster:

Arrange — Testdaten vorbereiten
Act — API-Anfrage ausführen
Assert — Ergebnis überprüfen

Insgesamt habe ich 19 Tests geschrieben, die alle erfolgreich bestanden haben:

CRUD-Tests (erstellen, lesen, aktualisieren, löschen)
Filtertests (nach Kategorie, Suchbegriff, Tag)
Fehlertests (404 für nicht vorhandene Ressourcen, 422 für ungültige Daten)
Tests für Statistiken, Tags und Kategorien

Verwendete Tools: VS Code, uv, FastAPI, Pydantic, pytest, requests



---

#### 2. 🚧 What challenges did I face?

Das größte technische Problem war, dass beim Starten des Course API der Port 8000 bereits durch den laufenden Notes-Server belegt war ([Errno 48] Address already in use). Außerdem hatte ich Schwierigkeiten mit zwei gleichnamigen main.py Dateien in verschiedenen Ordnern — der falsche Server wurde gestartet.
Beim Schreiben der Tests war es anfangs ungewohnt, dass jeder Test zunächst eine Notiz erstellen muss, bevor er sie testen kann. Ich musste verstehen, dass Tests unabhängig voneinander sein sollen und keine festen IDs voraussetzen dürfen.



---

#### 3. 💡 How did I overcome them?

Das Port-Problem habe ich gelöst, indem ich den laufenden Server mit kill $(lsof -t -i:8000) beendet habe. Das Problem mit den zwei gleichnamigen Dateien habe ich dadurch gelöst, dass ich das Course API direkt in die bestehende main.py integriert habe, anstatt eine separate Datei zu verwenden — das ist übersichtlicher und vermeidet Verwechslungen.
Für die Tests habe ich das Muster übernommen, zuerst eine Ressource zu erstellen und dann deren ID für weitere Operationen zu verwenden. So sind alle Tests vollständig unabhängig und funktionieren zuverlässig. Das Ausführen aller 19 Tests mit uv run pytest test_notes.py -v und das Sehen von "19 passed" war sehr befriedigend.



---

### Day 5

#### 1. ✅ What did I accomplish?

Am fünften Tag habe ich mich intensiv mit Pydantic-Validierung beschäftigt und die bestehenden API-Modelle deutlich robuster gemacht. Das Hauptziel war es, die API so zu gestalten, dass ungültige Daten bereits an der Eingabe abgefangen werden — bevor sie die Datenbank erreichen.
Theorie — Warum Validierung wichtig ist:
Ich habe verstanden, dass Typisierung allein nicht ausreicht. Ein Feld title: str akzeptiert zwar nur Strings, aber auch leere Strings, reine Leerzeichen oder extrem lange Texte. Echte Validierung bedeutet, Regeln für den Inhalt der Daten festzulegen.
Field(...) Constraints:
Ich habe Field(...) verwendet um folgende Einschränkungen zu definieren:

title: mindestens 3, maximal 100 Zeichen
content: mindestens 1, maximal 10.000 Zeichen
category: mit Beschreibung und erlaubten Werten
tags: maximal 10 Einträge, Standard leere Liste via default_factory=list

ConfigDict — Modellweite Einstellungen:
Ich habe ConfigDict mit zwei wichtigen Optionen verwendet:

str_strip_whitespace=True — entfernt automatisch führende und abschließende Leerzeichen aus allen String-Feldern
extra="forbid" — lehnt Anfragen mit unbekannten Feldern ab (z.B. Tippfehler wie tagz statt tags)

@field_validator — Eigene Validierungslogik:
Ich habe drei Field-Validators geschrieben:

title_not_whitespace — stellt sicher dass der Titel nach dem Trimmen noch mindestens 3 Zeichen hat
category_must_be_known — prüft ob die Kategorie in der erlaubten Liste ist (work, personal, school, ideas, general) und normalisiert sie zu Kleinbuchstaben
clean_tags — bereinigt Tags: Leerzeichen entfernen, Kleinbuchstaben, Duplikate entfernen, leere Tags ablehnen

@model_validator — Feldübergreifende Regel:
Ich habe einen Model-Validator implementiert der prüft ob eine work-Notiz auch den Tag work enthält. Diese Regel braucht Zugriff auf zwei Felder gleichzeitig (category und tags), weshalb ein @field_validator hier nicht ausreicht — ein @model_validator(mode="after") war die richtige Wahl.
NoteUpdate angepasst:
Die gleichen Constraints wurden auf NoteUpdate übertragen, wobei alle Felder Optional bleiben — ein leerer PATCH-Body {} ist weiterhin gültig.
Tag Modell gehärtet:
Das SQLModel Tag wurde mit min_length=2, max_length=30 und einem @field_validator ergänzt, der den Tag-Namen automatisch normalisiert.
Tests in test_validation.py:
Ich habe 12 Validierungstests geschrieben, alle erfolgreich bestanden:

Ablehnung von zu kurzem oder leerem Titel
Ablehnung unbekannter Kategorien
Normalisierung von Kategorien und Tags
Ablehnung von Extra-Feldern
Überprüfung der Work-Tag-Regel
PATCH mit leerem Body funktioniert
PATCH mit ungültigem Titel schlägt fehl

Verwendete Tools: VS Code, uv, FastAPI, Pydantic v2, pytest, requests



---

#### 2. 🚧 What challenges did I face?

Der schwierigste Moment war ein Fehler beim Starten des Servers:
TypeError: Field() got an unexpected keyword argument 'examples'
Das Argument examples wird in dieser Version von Pydantic nicht unterstützt. Da ich den Fehler zunächst nicht verstanden habe, musste ich die Fehlermeldung genau lesen um zu verstehen welches Argument das Problem verursacht.
Außerdem war der Unterschied zwischen @field_validator und @model_validator anfangs nicht sofort klar. Ich musste verstehen, wann man welchen verwendet — ein Field-Validator sieht immer nur ein einzelnes Feld, während ein Model-Validator Zugriff auf das gesamte Modell hat.



---

#### 3. 💡 How did I overcome them?

Den examples-Fehler habe ich behoben, indem ich das Argument einfach aus allen Field(...) Definitionen entfernt habe. Die Fehlermeldung hat dabei geholfen, da sie genau die Zeile und das problematische Argument angegeben hat.
Den Unterschied zwischen den Validator-Typen habe ich durch das Konspekt-Beispiel verstanden: die Work-Tag-Regel braucht sowohl category als auch tags — das ist nur mit @model_validator möglich. Diese praktische Anwendung hat das Konzept sofort klar gemacht.
Das häufige Ausführen von uv run pytest test_validation.py -v nach jeder Änderung hat mir geholfen, Fehler schnell zu erkennen und zu beheben.



---

### Day 6

#### 1. ✅ What did I accomplish?

Am sechsten Tag habe ich zwei Hauptthemen bearbeitet: Python-Dekoratoren und das Bestehen der vollständigen Test-Suite des Dozenten.
Dekoratoren — Theorie:
Ich habe verstanden, was Dekoratoren sind und wie sie funktionieren. Ein Dekorator ist eine Funktion, die eine andere Funktion "umwickelt" und ihr neues Verhalten hinzufügt, ohne den ursprünglichen Code zu verändern. Ich habe erkannt, dass ich Dekoratoren bereits die ganze Zeit verwendet habe — @app.get("/notes") und @field_validator("title") sind beides Dekoratoren.
class_based_decorator.py:
Ich habe eine neue Datei erstellt und drei verschiedene Arten von Dekoratoren implementiert:

log_decorator — ein einfacher funktionsbasierter Dekorator der Funktionsaufrufe loggt
TimerDecorator — ein klassenbasierter Dekorator der die Ausführungszeit misst
LogDecorator — ein klassenbasierter Dekorator der Argumente und Rückgabewerte loggt

Außerdem habe ich die icecream-Bibliothek verwendet (ic()), die Debugging-Output lesbarer macht als normales print().
Ich habe auch gelernt wie man kombinierte Dekoratoren verwendet — wenn zwei Dekoratoren übereinandergestapelt werden (@TimerDecorator + @LogDecorator), werden sie von innen nach außen ausgeführt.
Test-Suite des Dozenten:
Ich habe die offizielle Test-Suite test_main.py heruntergeladen und alle 70 Tests zum Bestehen gebracht. Dafür musste ich zwei Anpassungen vornehmen:

Den @model_validator der work-Tag-Regel entfernt, da die Tests des Dozenten work-Notizen ohne work-Tag erstellen
Datumsvalidierung in GET /notes hinzugefügt, damit ungültige Datumsformate wie not-a-date oder 2026-13-01 den Statuscode 422 zurückgeben

Endergebnis: 70 passed ✅
Verwendete Tools: VS Code, uv, FastAPI, pytest, requests, icecream



---

#### 2. 🚧 What challenges did I face?

Das erste Problem war beim Starten der Test-Suite — alle Tests wurden als SKIPPED angezeigt, weil der Server nicht lief. Ich musste lernen, zwei Terminals gleichzeitig zu verwalten: eines für den laufenden Server und eines für die Tests.
Das zweite Problem war mit der Datumsvalidierung. Mein erster Regex ^\d{4}-\d{2}-\d{2}$ mit $ am Ende blockierte auch gültige Daten, die zusätzlich eine Uhrzeit enthielten (z.B. 2026-05-10T08:33:00). Die Tests des Dozenten verwenden datetime.now().isoformat() welches immer Datum + Uhrzeit zurückgibt — deshalb schlugen die Tests fehl.
Das dritte Problem war der @model_validator für work-Notizen. Diese Regel war zwar aus Validierungssicht korrekt, kollidierte aber mit den Test-Daten des Dozenten, der work-Notizen ohne work-Tag erstellt.



---

#### 3. 💡 How did I overcome them?

Das Server-Problem habe ich gelöst, indem ich gelernt habe, mehrere Terminals in VS Code gleichzeitig zu verwenden — einen für uv run fastapi dev main.py und einen anderen für uv run pytest test_main.py -v.
Den Regex-Fehler habe ich durch genaues Lesen des Test-Codes verstanden. Ich habe gesehen dass der Test datetime.now().isoformat() verwendet, was ein vollständiges ISO-Datetime-Format zurückgibt. Die Lösung war einfach: das $ am Ende des Regex entfernen, damit sowohl 2026-05-10 als auch 2026-05-10T08:33:00 akzeptiert werden.
Für den model_validator Konflikt habe ich entschieden, die Regel zu entfernen — die Test-Suite des Dozenten ist die Referenz, und das Bestehen aller 70 Tests hatte Priorität.
Das schrittweise Vorgehen — Tests ausführen, Fehler lesen, eine Sache fix, wieder testen — war die effektivste Strategie um von 17 Fehlern auf 0 zu kommen.



---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?

Am siebten Tag habe ich zum ersten Mal ein Frontend für meine Notes API gebaut — mit Streamlit, einer Python-Bibliothek die es ermöglicht, Web-Interfaces ohne HTML oder JavaScript zu erstellen.
Streamlit — Theorie:
Ich habe verstanden was Streamlit ist und warum es besonders für Backend-Entwickler nützlich ist. Statt HTML, CSS und JavaScript zu lernen, kann man mit reinem Python interaktive Webanwendungen bauen. Streamlit läuft als separater Server (Port 8501/8502) und kommuniziert mit der FastAPI (Port 8000).
Say No App (say_no.py):
Als erste Übung habe ich eine Test-App gebaut die eine externe API (naas.isalman.dev/no) aufruft und lustige Ablehnungsgründe anzeigt. Dabei habe ich folgende Streamlit-Konzepte gelernt:

st.text_input() — Texteingabefeld
st.button() — Knopf der Aktionen auslöst
st.write() — Text ausgeben
st.session_state — Zustand zwischen Interaktionen speichern
st.expander() — aufklappbarer Bereich

Notes App Frontend (frontend.py):
Das Hauptprojekt des Tages war ein vollständiges Frontend für die Notes API mit zwei Funktionen:
Funktion 1 — Alle Notizen anzeigen:

Dropdown-Liste mit allen Notiz-Titeln
Bei Auswahl werden Titel, Kategorie, Tags, Erstellungsdatum und Inhalt angezeigt
Daten werden live von der FastAPI geladen

Funktion 2 — Neue Notiz erstellen:

Formular mit st.form() für gemeinsame Eingabe aller Felder
Felder: Title (st.text_input), Content (st.text_area), Category (st.selectbox), Tags (st.text_input)
Nach erfolgreichem Erstellen wird die Seite automatisch neu geladen (st.rerun()) und die neue Notiz erscheint sofort in der Liste

Verwendete Tools: VS Code, uv, Streamlit, FastAPI, requests



---

#### 2. 🚧 What challenges did I face?

Das größte Problem war die Verwaltung von mehreren gleichzeitig laufenden Prozessen. Für die Notes App müssen drei Dinge gleichzeitig laufen:

FastAPI Server auf Port 8000
Streamlit Server auf Port 8501/8502
Browser

Ich habe mehrfach vergessen den FastAPI Server zu starten, was zu einem ConnectionError in Streamlit führte. Außerdem war es anfangs verwirrend dass say_no.py und frontend.py auf verschiedenen Ports laufen (8501 und 8502).



---

#### 3. 💡 How did I overcome them?

Ich habe gelernt immer zuerst den FastAPI Server zu starten und dann erst Streamlit. Die Fehlermeldung Connection refused port 8000 war dabei sehr hilfreich — sie zeigte genau welcher Server fehlt.
Für die Port-Verwechslung habe ich gelernt immer im Terminal nachzuschauen welcher Local URL angezeigt wird — dort steht der genaue Port auf dem Streamlit läuft.
Das st.form() Konzept war sehr praktisch — es ermöglicht alle Eingaben zusammen mit einem einzigen Button abzuschicken, was die Benutzererfahrung deutlich verbessert.



---

### Day 8

#### 1. ✅ What did I accomplish?

Am achten Tag habe ich mein Projekt finalisiert und für die Abgabe vorbereitet. Der Schwerpunkt lag nicht auf neuer Funktionalität, sondern auf Qualitätssicherung, Dokumentation und Projektorganisation.
Finale Überprüfung der drei Hauptbefehle:
Ich habe sichergestellt, dass alle drei vom Dozenten vorgegebenen Befehle fehlerfrei funktionieren:

uv run fastapi dev main.py — Backend startet ohne Fehler
uv run pytest test_main.py -v — alle 70 Tests bestehen
uv run streamlit run frontend.py — Frontend lädt korrekt

Frontend zusammengeführt:
Die Say-No-App (say_no.py) und die Notes-App (frontend.py) wurden in eine einzige Datei frontend.py zusammengeführt, da der Dozent nur diese eine Datei prüft. Das finale Frontend enthält beide Funktionen übersichtlich in einer Datei.
README.md erstellt:
Ich habe eine vollständige Projektdokumentation auf Deutsch geschrieben. Das README enthält:

Projektbeschreibung und Übersicht
Schnellstart-Anleitung mit allen drei Befehlen
Vollständige Tabelle aller API-Endpunkte
Beschreibung aller Filterparameter
Validierungsregeln mit Beispielen
Datenbankstruktur (Many-to-Many)
Entwicklungszeitlinie über alle 7 Kurstage
Technologie-Stack

Projektstruktur aufgeräumt:
Ich habe überprüft ob alle wichtigen Dateien im Repository vorhanden und aktuell sind:

main.py — vollständiges Backend
frontend.py — Streamlit-Frontend
test_main.py — Referenz-Testsuite
test_notes.py — eigene Tests
test_validation.py — Validierungstests
work-log-template.md — Lerntagebuch
README.md — Projektdokumentation

Git — finaler Push:
Alle Änderungen wurden mit aussagekräftigen Commit-Messages versioniert und auf GitHub gepusht.
Verwendete Tools: VS Code, Git, GitHub, uv, FastAPI, Streamlit, pytest



---

#### 2. 🚧 What challenges did I face?

Die größte Herausforderung war die Qualitätssicherung — sicherzustellen dass alle drei Befehle in der richtigen Reihenfolge und ohne Fehler funktionieren. Dabei musste ich immer daran denken, zuerst den FastAPI-Server zu starten, bevor ich Tests oder das Frontend ausführe.
Beim Zusammenführen der zwei Streamlit-Dateien musste ich darauf achten, dass beide Teile unabhängig voneinander funktionieren und die session_state-Variablen sich nicht gegenseitig beeinflussen.
Das Schreiben des README war zeitaufwändig — es war wichtig, alle relevanten Informationen vollständig und klar zu dokumentieren, ohne zu viel oder zu wenig zu erklären.



---

#### 3. 💡 How did I overcome them?

Für die Qualitätssicherung habe ich eine feste Reihenfolge eingehalten: zuerst Backend starten, dann Tests ausführen, dann Frontend testen. Diese Routine hat mir geholfen, keine Schritte zu überspringen.
Das Zusammenführen der Streamlit-Dateien war einfacher als erwartet — ich habe einen st.divider() zwischen beiden Teilen eingefügt um sie visuell zu trennen, und die session_state-Schlüssel haben unterschiedliche Namen, sodass es keine Konflikte gibt.
Für das README habe ich mich an der Struktur der API-Dokumentation orientiert die wir während des Kurses kennengelernt haben — klare Abschnitte, Tabellen für Endpunkte und Codebeispiele für Datenformate.



---

