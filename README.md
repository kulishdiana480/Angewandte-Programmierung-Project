# Notizen-API – Angewandte Programmierung
**Hochschule Coburg | Wirtschaftsinformatik | Diana Kulish**

---

## Über das Projekt

Dieses Repository dokumentiert meine Arbeit im Kurs Angewandte Programmierung.
Über 7 Kurstage habe ich eine vollständige Notiz-Anwendung entwickelt –
von einfachen API-Endpunkten bis hin zu einer Datenbankanwendung mit Frontend.

Das Projekt besteht aus einem FastAPI-Backend, einer SQLite-Datenbank,
automatisierten Tests und einem Streamlit-Frontend.

---

## Schnellstart

**Schritt 1 – Backend starten:**
```bash
uv run fastapi dev main.py
```

**Schritt 2 – Frontend starten (zweites Terminal):**
```bash
uv run streamlit run frontend.py
```

**Schritt 3 – Tests ausführen (Backend muss laufen):**
```bash
uv run pytest test_main.py -v
```

> Die interaktive API-Dokumentation ist unter `http://127.0.0.1:8000/docs` erreichbar.

---

## Dateien im Repository

| Datei | Beschreibung |
|-------|-------------|
| `main.py` | FastAPI-Backend mit allen Endpunkten und Datenbanklogik |
| `frontend.py` | Streamlit-Frontend mit Say-No-App und Notizen-Oberfläche |
| `test_main.py` | Referenz-Testsuite des Dozenten (70 Tests) |
| `test_notes.py` | Eigene CRUD-Tests (19 Tests) |
| `test_validation.py` | Tests für Pydantic-Validierung (12 Tests) |
| `class_based_decorator.py` | Übungen zu Python-Dekoratoren |
| `work-log-template.md` | Tägliches Lerntagebuch |
| `data/notes.json` | Ausgangsdaten (beim ersten Start automatisch migriert) |
| `notes.db` | SQLite-Datenbank |
| `my-first-api/main.py` | Course-API-Übung aus Tag 4 |

---

## Was die Anwendung kann

**Notizen verwalten:**
- Notiz erstellen, abrufen, aktualisieren (PUT/PATCH) und löschen
- Alle Notizen auflisten

**Filtern und Suchen:**
- Nach Kategorie, Tag oder Suchbegriff filtern
- Nach Erstellungsdatum filtern (`created_after`, `created_before`)
- Mehrere Filter gleichzeitig kombinieren

**Zusätzliche Ressourcen:**
- Tags als eigene Ressource verwalten
- Kategorien als eigene Ressource verwalten
- Statistiken abrufen (Gesamtanzahl, nach Kategorie, Top-Tags)

**Frontend:**
- Notizen in einer Dropdown-Liste anzeigen
- Neue Notizen per Formular erstellen

---

## API-Endpunkte

### Notizen
| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| POST | `/notes` | Neue Notiz erstellen |
| GET | `/notes` | Alle Notizen auflisten (mit Filtern) |
| GET | `/notes/{id}` | Einzelne Notiz abrufen |
| PUT | `/notes/{id}` | Notiz vollständig ersetzen |
| PATCH | `/notes/{id}` | Notiz teilweise aktualisieren |
| DELETE | `/notes/{id}` | Notiz löschen |
| GET | `/notes/stats` | Statistiken abrufen |

### Tags & Kategorien
| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| GET | `/tags` | Alle Tags auflisten |
| GET | `/tags/{name}/notes` | Notizen mit bestimmtem Tag |
| GET | `/categories` | Alle Kategorien auflisten |
| GET | `/categories/{name}/notes` | Notizen einer Kategorie |

### Filterparameter für `GET /notes`
| Parameter | Beschreibung |
|-----------|-------------|
| `category` | Nach Kategorie filtern |
| `search` | In Titel und Inhalt suchen |
| `tag` | Nach Tag filtern |
| `created_after` | Nur Notizen nach diesem Datum |
| `created_before` | Nur Notizen vor diesem Datum |

---

## Datenformat

```json
{
  "id": 1,
  "title": "Teambesprechung",
  "content": "Q2-Ziele mit dem Kunden besprechen",
  "category": "work",
  "tags": ["meeting", "urgent"],
  "created_at": "2026-01-01T10:00:00Z"
}
```

**Erlaubte Kategorien:** `work` · `personal` · `school` · `ideas` · `general`

---

## Validierung

Alle Eingaben werden automatisch durch Pydantic geprüft.
Ungültige Anfragen erhalten den Statuscode **422 Unprocessable Entity**.

| Feld | Regel |
|------|-------|
| `title` | Pflichtfeld, 3–100 Zeichen |
| `content` | Pflichtfeld, 1–10.000 Zeichen |
| `category` | Muss ein erlaubter Wert sein |
| `tags` | Maximal 10 Tags, je mindestens 2 Zeichen |

Tags werden automatisch bereinigt:
`["URGENT", "urgent", " meeting "]` → `["urgent", "meeting"]`

Unbekannte Felder werden abgelehnt (`extra="forbid"`).

---

## Datenbankstruktur

Die Anwendung verwendet **SQLite** mit **SQLModel**.

Drei Tabellen:
- `notes` – alle Notizen
- `tags` – eindeutige Tags
- `notetaglink` – Verknüpfungstabelle (Many-to-Many)

Beim ersten Start werden vorhandene Daten aus `data/notes.json`
automatisch in die Datenbank migriert.

---

## Verwendete Technologien

| Technologie | Zweck |
|-------------|-------|
| FastAPI | REST-API Framework |
| SQLModel | ORM (Pydantic + SQLAlchemy) |
| SQLite | Datenbank |
| Pydantic v2 | Datenvalidierung |
| Streamlit | Frontend |
| pytest | Automatisierte Tests |
| uv | Paketverwaltung |
| icecream | Debug-Ausgaben |

---

## Lernprozess

Das Projekt wurde schrittweise über 7 Kurstage aufgebaut:

| Tag | Thema |
|-----|-------|
| 1 | FastAPI Setup, erste Endpunkte |
| 2 | Python-Grundlagen, dateibasierte Notizen-API |
| 3 | REST-Design, vollständiges CRUD, SQLite-Migration |
| 4 | POST-Endpunkte, Course-API, pytest-Tests |
| 5 | Pydantic-Validierung, Field-Constraints, Validators |
| 6 | Python-Dekoratoren, Referenz-Testsuite (70/70) |
| 7 | Streamlit-Frontend |

Mehr Details zum Lernprozess, aufgetretenen Problemen und deren Lösungen
sind im `work-log-template.md` dokumentiert.