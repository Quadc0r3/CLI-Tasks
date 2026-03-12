# KI-Interaktionsprotokoll

Dokumentation aller KI-Interaktionen (Claude) im Rahmen der Bachelorarbeit.  
Erfasst sind Prompts, Antwortform und Qualitätsbewertung je Task der KI-Bedingung.

> Alle Interaktionen erfolgten mit **Claude Sonnet** über die Weboberfläche claude.ai.

---

## Übersicht

| Task | Name | Phase | Iterationen | Prompts |
|------|------|-------|-------------|---------|
| [Task 1](#task-1--produktvision-und-scope) | Produktvision und Scope | Requirements & Planung | 1 | 1 |
| [Task 3](#task-3--akzeptanzkriterien) | Akzeptanzkriterien | Requirements & Planung | 1 | 2 (inkl. Rückfragen) |
| [Task 6](#task-6--datenmodell) | Datenmodell | Architektur & Design | 2 | 2 (inkl. Rückfragen) |
| [Task 8](#task-8--persistenzkonzept) | Persistenzkonzept | Architektur & Design | 1 | 2 (inkl. Rückfragen) |
| [Task 9](#task-9--task-erstellen) | Task erstellen | Implementierung Kernfunktion | 1 | 2 (inkl. Rückfragen) |
| [Task 11](#task-11--status-ändern) | Status ändern | Implementierung Kernfunktion | 1 | 2 (inkl. Rückfragen) |
| [Task 14](#task-14--task-löschen) | Task löschen | Erweiterung | 1 | 2 (inkl. Rückfragen) |
| [Task 16](#task-16--unit-tests) | Unit Tests | Testing | 3 | 4 (inkl. Fehlerkorrektur) |
| [Task 18](#task-18--refactoring) | Refactoring | Qualität & Wartung | 1 | 1 |
| [Task 20](#task-20--code-review) | Code Review | Qualität & Wartung | 1 | 1 |

---

## Task 1 — Produktvision und Scope

**Phase:** Requirements & Planung | **Bedingung:** Mit KI | **Dauer:** 46 min | **Anforderungen erfüllt:** 90 %  
**Eingenommene Rolle:** Evaluator

### Prompt

```
Hey, ich mache ein Projekt im Software Development Life Cycle (SDLC) und gehe da die Phasen
Requirements & Planung, Architektur & Design, Implementierung Kernfunktion, Erweiterung,
Testing und Qualität & Wartung durch. Zu jeder Phase gibt es mehrere Tasks zu machen.

Die Projektidee ist, eine Task-Anwendung (CLI) in Python zu schreiben.

Jetzt ist der erste Task, er geht um die Produktvision und den Scope der Anwendung.
Dies soll nun definiert werden.

Kannst du diesen ersten Task bearbeiten?
```

### Antwort

Generiertes Word-Dokument (`Produktvision_CLI_TaskManager.docx`) mit Zielgruppe, In-Scope, Out-of-Scope, Technologie-Stack, Erfolgskriterien und Risikoabschätzung.

### Qualitätsbewertung

| Kriterium | Bewertung |
|---|---|
| Zielgruppe | Gut definiert — IT-affine Nutzende |
| In-Scope | CRUD und JSON-Persistenz korrekt erkannt |
| Out-of-Scope | Teilweise sinnvoll (GUI, recurring Tasks), teilweise überdimensioniert (Sync zweifach erwähnt, Kalenderintegration) |
| Technologie-Stack | Python 3.10+ statt 3.14 angegeben — nicht aktuell |
| Risikobewertung | Widerspruch: Scope-Creep erwähnt, gleichzeitig Multiplattformkompatibilität als Anforderung gelistet |

### Reflexionsnotiz

> „KI generierte eine sehr vollständige Vision. Allerdings enthielt sie frühe Architekturentscheidungen und konservative Technologieannahmen, die kritisch geprüft werden mussten. Die Rolle verschob sich von Autor zu Evaluator."

---

## Task 3 — Akzeptanzkriterien

**Phase:** Requirements & Planung | **Bedingung:** Mit KI | **Dauer:** 32 min | **Anforderungen erfüllt:** 96 %  
**Eingenommene Rolle:** Evaluator

### Prompt

```
Hey, ich habe dir hier für das gleiche Projekt nun die leicht angepasste Produktvision
und die von mir erstellten User Stories. Bitte beachte diese. Ich möchte, dass du mir
als Software-Development-Lead und Projektmanager ein Dokument mit den Akzeptanzkriterien
für dieses Programm entwirfst. Es soll dabei realistisch bleiben.

Stelle mir, bevor du das machst, noch max. 10 Fragen, damit du dieses bestmöglich erstellen kannst.
```

### Rückfragen & Antworten

| Frage | Antwort |
|---|---|
| In welchem Format sollen die Akzeptanzkriterien formuliert werden? | Given/When/Then (Gherkin-Stil) |
| Soll jede der 16 User Stories eigene Kriterien bekommen, oder sollen thematisch ähnliche zusammengefasst werden? | Beides — gruppiert mit Verweis auf Stories |
| Wie soll das Dokument genutzt werden? | Als Grundlage für Testfälle (QA), als Definition of Done, zur Abnahme durch Stakeholder |

### Qualitätsbewertung

| Kriterium | Bewertung |
|---|---|
| Strukturelle Vollständigkeit | Hoch |
| Redaktioneller Feinschliff | Gering — vereinzelte Formatierungsfehler (Leerseiten, inkonsistente Bezeichnungen AC/AK) |
| Terminologie | Teilweise englisch statt deutsch (AC statt AK) |
| Präzision | Vereinzelte Unschärfen (z. B. fehlende Zielangabe beim Edit-Feld) |
| Umlaute | Fehler vorhanden — „Übergang" als „Ubergang" |

### Reflexionsnotiz

> „Die inhaltliche Breite der Kriterien reduzierte den initialen Strukturierungsaufwand, erforderte jedoch eine kritische Nachschärfung einzelner Präzisierungen und Terminologien. Die Aufgabe bestand primär in Validierung und Qualitätskontrolle statt in kreativer Ausarbeitung."

---

## Task 6 — Datenmodell

**Phase:** Architektur & Design | **Bedingung:** Mit KI | **Dauer:** 50 min | **Anforderungen erfüllt:** 98 %  
**Eingenommene Rolle:** Evaluator

### Prompt

```
Hey, jetzt sind wir in der 2. Phase — Architektur und Design. Ich habe dafür bereits die
Modulstruktur erstellt, jetzt ist es die Aufgabe (Task 6) von dir dazu das Datenmodell
zu erstellen. Noch immer bist du Projektmanager und Product Owner.

Falls nötig, stelle mir Fragen, damit du dieses Modell bestmöglich erstellen kannst.
```

### Rückfragen & Antworten

| Frage | Antwort |
|---|---|
| Welches Ausgabeformat soll das Datenmodell haben? | Word-Dokument (.docx) mit Beschreibung & Tabellen |
| Soll eine visuelle Darstellung der Datenstruktur enthalten sein? | Ja, als separates Bild/SVG |

### Qualitätsbewertung

| Kriterium | Bewertung |
|---|---|
| Zeitstempel (created_at, updated_at) | Korrekt antizipiert |
| Enumerations | Enum englisch, JSON-Strings deutsch — inkonsistent |
| Backup-Mechanismus | Erwähnt, aber nicht beschrieben |
| Scope | Leicht overengineered (Tags als Erweiterungsfeld) |
| SVG/ERM | Erstellt, aber in separatem Dokument — nicht direkt sichtbar |

### Reflexionsnotiz

> „Statt alles mühsam selbst formal auszuarbeiten, konnte ich in eine evaluierende, kritisch prüfende Position wechseln, was die Arbeit deutlich effizienter, aber auch analytisch anspruchsvoller gemacht hat."

---

## Task 8 — Persistenzkonzept

**Phase:** Architektur & Design | **Bedingung:** Mit KI | **Dauer:** 36 min | **Anforderungen erfüllt:** 100 %  
**Eingenommene Rolle:** Evaluator

### Prompt

```
Hey, jetzt geht es an Task 8 „Persistenzkonzept", den letzten der Phase 2.
Erweitere dabei das im Task 6 erstellte Datenmodell um ein neues Speicherkonzept,
in einer neuen Datei, die rundum die Persistenz der Tasks vollumfänglich beschreibt.

Wenn es Fragen gibt, dann stelle sie bitte.
```

### Rückfragen & Antworten

| Frage | Antwort |
|---|---|
| Wo soll die tasks.json standardmäßig gespeichert werden? | Konfigurierbar via Umgebungsvariable (Fallback auf `~/.tasktool/`) |
| Soll ein automatisches Backup vor jedem Schreibvorgang erstellt werden? | Ja, als `tasks.json.bak` |

### Qualitätsbewertung

Alle 8 Vorschläge übernommen, keine verworfen. Hohe strukturelle Qualität, alle Anforderungen vollständig erfüllt.

### Reflexionsnotiz

> „Beim Persistenzkonzept habe ich besonders gemerkt, wie stark die KI in Robustheit und Produktionsreife denkt — deutlich strukturierter und defensiver, als ich es für ein Studienprojekt ursprünglich geplant hätte."

---

## Task 9 — Task erstellen

**Phase:** Implementierung Kernfunktion | **Bedingung:** Mit KI | **Dauer:** 54 min | **Anforderungen erfüllt:** 80 %  
**Eingenommene Rolle:** Evaluator

### Prompt

```
Hey, wir befinden uns in Phase 3 „Implementierung Kernfunktion". Es existiert aktuell
noch kein produktiver Code im Projekt.
Deine Aufgabe (Task 9) ist es, ausschließlich die Kernfunktion „Task erstellen" zu implementieren.

Du agierst in der Rolle eines Software Engineers und hältst dich strikt an:
  * das definierte Datenmodell (Task 6)
  * das Persistenzkonzept (Task 8)
  * das CLI-Interaktionsdesign
  * die definierte Modulstruktur

Nicht zu implementieren sind:
  * Task bearbeiten / Status ändern / JSON-Speicherung (nur vorbereiten, falls notwendig)
  * Filterfunktion / Prioritätensystem / Logging / Unit-Tests
  * Edge-Case-Behandlung über grundlegende Validierung hinaus

Der Code wird bewertet anhand von: LOC, Cyclomatic Complexity, Maintainability Index,
Code Smells, Bugs, Erfüllung der funktionalen Anforderungen.

Implementiere nur das, was für „Task erstellen" notwendig ist.
Erzeuge lauffähige Python-Dateien gemäß Modulstruktur.
Stelle mir vor der Implementierung gezielte Rückfragen, falls Annahmen notwendig sind.
```

### Rückfragen & Antworten

| Frage | Antwort |
|---|---|
| Welche Felder soll der Create-Wizard abfragen? | Titel (Pflicht), Beschreibung (optional), Priorität (optional, default: mid) |
| Welches CLI-Framework soll verwendet werden? | argparse (stdlib, keine externen Abhängigkeiten) |

### Ergebnis (Codemetriken)

| Metrik | Wert |
|---|---|
| LOC | 241 |
| Avg. Cyclomatic Complexity | 1,89 |
| Max. Cyclomatic Complexity | 5 |
| Avg. Maintainability Index | 46,1 |
| Code Smells | 0 |
| Bugs | 0 |

### Auffälligkeit

Die KI implementierte eine vollständige `serialize.py` inklusive JSON-Persistenzlogik, obwohl dies explizit **nicht** zum Scope von Task 9 gehörte. Dies führte zur Anlage eines separaten Branches (`main-ki-serialize`) und zur manuellen Neuimplementierung in Task 12.

### Reflexionsnotiz

> „Die KI erzeugt strukturell hochwertigen und gut organisierten Code, tendiert jedoch dazu, zukünftige Anforderungen vorwegzunehmen und damit definierte Scope-Grenzen zu überschreiten."

---

## Task 11 — Status ändern

**Phase:** Implementierung Kernfunktion | **Bedingung:** Mit KI | **Dauer:** 24 min | **Anforderungen erfüllt:** 100 %  
**Eingenommene Rolle:** Evaluator

### Prompt

```
Wir befinden uns weiterhin in Phase 3 „Implementierung Kernfunktion".

Du agierst in der Rolle eines Software Engineers und hältst dich strikt an alle
im Requirements Engineering definierten Entscheidungen sowie die bestehende Modulstruktur.

Aufgabe (Task 11): Implementiere die Funktionalität „Status ändern" inklusive
des definierten Workflows.

Wichtig:
  - Der bestehende Code soll angepasst und erweitert werden.
  - Keine komplette Neustrukturierung des Projekts.
  - Keine zusätzlichen Features außerhalb der Statusänderung.
  - Persistenz nur im Rahmen des bereits definierten Konzepts.

Statusübergänge nur gemäß der im RE definierten Zustandslogik.
Ungültige Übergänge müssen abgefangen werden.

Gib mir die vollständigen, angepassten Python-Dateien aus.
Stelle vor der Implementierung gezielte Rückfragen.
```

### Rückfragen & Antworten

| Frage | Antwort |
|---|---|
| Soll `done` und `reopen` als separate Befehle oder als generischer `status`-Befehl implementiert werden? | done + reopen (2 separate Befehle, gemäß Interaktionsdesign) |
| Soll `IN_PROGRESS → DONE` direkt via `done` möglich sein? | Ja, direkt erlaubt |

### Ergebnis (Codemetriken)

| Metrik | Wert |
|---|---|
| LOC (kumuliert) | 335 (+34) |
| Avg. Cyclomatic Complexity | 1,97 |
| Max. Cyclomatic Complexity | 7 |
| Avg. Maintainability Index | 40,9 |
| Code Smells | 2 |
| Bugs | 0 |

### Reflexionsnotiz

> „Durch meine eigene Vorarbeit war die Qualitätskontrolle deutlich effizienter, da Architekturverständnis und Debugging-Fokus bereits vorhanden waren."

---

## Task 14 — Task löschen

**Phase:** Erweiterung | **Bedingung:** Mit KI | **Dauer:** 19 min | **Anforderungen erfüllt:** 90 %  
**Eingenommene Rolle:** Evaluator

### Prompt

```
Hey, jetzt bist du mit Task 14 in Phase 4 „Erweiterung" dran.
Du bist weiterhin in der Rolle als Software Engineer.

Deine Aufgabe ist es, die Task-Löschfunktion zu implementieren.
Relevant aus dem CLI-Interaktionsdesign:

  delete [id]       -> löscht einen Task anhand der ID
  delete --all      -> löscht alle Tasks
  delete --done     -> löscht alle erledigten Tasks

Passe dafür den aktuellen Code an und nutze möglichst die bereits vorhandenen Funktionen.
Gib mir bitte die vollständigen Python-Dateien, die geändert werden müssen.
```

### Rückfragen & Antworten

| Frage | Antwort |
|---|---|
| Sicherheitsabfrage bei `delete [id]`? | Immer Sicherheitsabfrage (auch bei DONE) |
| Gleiches Verhalten für `--all` und `--done`? | Ja, immer Sicherheitsabfrage |

### Ergebnis (Codemetriken)

| Metrik | Wert |
|---|---|
| LOC (kumuliert) | 452 (+80) |
| Avg. Cyclomatic Complexity | 2,11 |
| Max. Cyclomatic Complexity | 11 |
| Avg. Maintainability Index | 37,2 |
| Code Smells | 4 |
| Bugs | 1 |

### Reflexionsnotiz

> „Die KI konnte die funktionale Anforderung schnell umsetzen, zeigte jedoch Schwächen bei der Integration in die bestehende Architektur. Eine sorgfältige manuelle Code-Review bleibt weiterhin notwendig."

---

## Task 16 — Unit Tests

**Phase:** Testing | **Bedingung:** Mit KI | **Dauer:** 28 min | **Anforderungen erfüllt:** 90 %  
**Eingenommene Rolle:** Ko-Autor | **Iterationen:** 3

### Prompt

```
Hey, wir sind jetzt bei Task 16: Unit Tests. Deine Rolle bleibt Software Engineer.
Implementiere Unit Tests für den aktuellen Code-Stand des CLI-Tasktools.

Anforderungen:
  * Verwende pytest.
  * Teste die wichtigsten Kernfunktionen im Service-Layer.
  * CLI-Parsing muss nicht vollständig getestet werden.
  * Tests sollen klar strukturiert, wartbar und möglichst isoliert sein.
  * Verwende Mocking, falls File-I/O betroffen ist.

Stelle mir Fragen, falls dir für sinnvolle Tests Informationen fehlen.
```

### Rückfragen & Antworten

| Frage | Antwort |
|---|---|
| Wo soll die Test-Datei liegen? | `tests/test_task_service.py` (eigener Ordner) |
| Sollen `serialize.py`-Funktionen direkt getestet werden? | Ja, auch `serialize.py` direkt testen (read/write mit tmp-Datei) |

### Fehlerkorrektur (Iteration 2–3)

Beim ersten Ausführen trat ein `ModuleNotFoundError` auf (`import serialize` nicht gefunden). Die KI lieferte die korrekte Lösung: eine `pytest.ini` mit `pythonpath = .` im Root-Verzeichnis.

```
[pytest]
testpaths = tests
pythonpath = .
```

### Ergebnis (Codemetriken)

| Metrik | Wert |
|---|---|
| LOC Produktivcode | 512 (+2) |
| LOC Testcode | 353 (neu) |
| Testabdeckung | 65 % |
| Code Smells | 6 |
| Bugs | 0 |

### Reflexionsnotiz

> „Die KI konnte sehr schnell eine umfangreiche und gut strukturierte Testsuite erzeugen. Gleichzeitig zeigte sich, dass KI-generierter Code häufig zusätzliche Nacharbeit bei Projektkonfiguration, Codequalität und Scope-Kontrolle benötigt."

---

## Task 18 — Refactoring

**Phase:** Qualität & Wartung | **Bedingung:** Mit KI | **Dauer:** 35 min | **Anforderungen erfüllt:** 95 %  
**Eingenommene Rolle:** Evaluator

### Prompt

Der Prompt umfasste eine vollständige Refactoring-Anforderungsliste mit folgenden Schwerpunkten:

- Cyclomatic Complexity reduzieren
- Maintainability Index erhöhen
- Lesbarkeit und Struktur verbessern
- Code-Duplikate entfernen (DRY-Prinzip)
- Logik zwischen Modulen klarer trennen

Zusätzlich wurden 7 konkrete Bugfixes aus dem Edge-Case-Testing (Task 17) übergeben, u. a.:
- Editieren eines nicht existierenden Tasks → Edit-Maske erscheint trotzdem
- `Ctrl + C` erzeugt Traceback statt sauber zu beenden
- Korruptes JSON führt zu ungefangenem Fehler
- Negative `last_id` wird akzeptiert
- Fehlende `.env` Datei wird nicht behandelt

### Ergebnis (Codemetriken)

| Metrik | Wert |
|---|---|
| LOC (kumuliert) | 568 (+56) |
| Avg. Cyclomatic Complexity | 2,09 |
| Max. Cyclomatic Complexity | 7 |
| Avg. Maintainability Index | 34,6 |
| Testabdeckung | 65 % |
| Code Smells | 5 |
| Bugs | 0 |

### Reflexionsnotiz

> „Das Refactoring durch Claude hat den Code deutlich strukturierter und wartbarer gemacht. Trotzdem zeigt sich, dass KI beim Refactoring zwar strukturelle Verbesserungen gut umsetzt, aber nicht immer alle bestehenden Tests und Randfälle vollständig berücksichtigt."

---

## Task 20 — Code Review

**Phase:** Qualität & Wartung | **Bedingung:** Mit KI | **Dauer:** 27 min | **Anforderungen erfüllt:** 90 %  
**Eingenommene Rolle:** Evaluator

### Prompt

Vollständiges Code Review mit 10 definierten Analysebereichen:

1. Architektur & Separation of Concerns
2. Implementierte Funktionen (Vollständigkeit)
3. Unbenutzter Code (Imports, Variablen, Funktionen)
4. Codequalität (Lesbarkeit, Namenskonventionen, Komplexität)
5. Fehlerbehandlung und Robustheit
6. Risiken für Stabilität und Datenintegrität
7. Wartbarkeit (Modularität, Testbarkeit, Kopplung)
8. Tests (Abdeckung, fehlende Edge Cases)
9. Mögliche Refactorings
10. Zusammenfassung (Stärken, Risiken, Top-3-Maßnahmen)

### Qualitätsbewertung

Alle Vorschläge übernommen. Besonders auffällig: Ein `Enum-TypeError` in `_sort()` wurde vom Review nicht erwähnt, obwohl der Codepfad erreichbar ist.

### Reflexionsnotiz

> „Der Task lief strukturiert ab: Review lesen, Code gegenlesen, Kritik formulieren. Die interessanteste Stelle war der Enum-TypeError-Befund, der im Review nicht erwähnt wurde — ob der tatsächlich auftritt, hängt davon ab, ob `_sort()` mit priority oder status jemals aufgerufen wird, was im Code möglich ist."

---

*Quelle: Eigene Darstellung / Forschungsprotokoll*
