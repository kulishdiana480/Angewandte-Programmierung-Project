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






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 5

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 6

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













