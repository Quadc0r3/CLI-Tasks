# Tasktool - CLI Task Manager

Das Tasktool ist ein rudimentärer Task-Manager komplett in der Kommandozeile. Es ermöglicht es diverse Aufgaben mit
Titel, Beschreibung, und Priorität zu tracken, sowie diese zu bearbeiten, deren Status zu ändern, und zu löschen.
Gebaut wurde es im Rahmen meiner Bachelorarbeit, in welcher ich den Einfluss von generativer KI in den Software
Development Lifecycle untersuche. Es wurde von mir und Claude Sonett 4.6 von Anthropic entwickelt.

## Quickstart

```bash
git clone https://github.com/username/task-manager.git
cd task-manager
python task_tool.py create
```

## Features

* ```create``` - Task mit Wizard erstellen
* ```edit```   - Task mit Wizard bearbeiten
* ```show [id]```   - Details zum Task anzeigen
* ```done [id]``` - Task auf Status 'abgeschlossen' setzen
* ```reopen [id]``` - abgeschlossen Status auf 'offen' setzen
* ```list``` - alle Tasks anzeigen. Sortierung und Filterung möglich.
* ```delete``` - Task löschen

## Voraussetzungen

- Python 3.12 oder neuer

## Installation

Repository klonen:

```bash
git clone https://github.com/username/task-manager.git
cd task-manager
```

## Nutzung

Das Tasktool wird über die Kommandozeile benutzt:

```bash
python task_tool.py --help
```

## Beispiele

Übersicht über alle Befehle

```bash
python task_tool.py
python task_tool.py show -h
```

Task erstellen

```bash
python task_tool.py create
```

Task mit der ID 1 anzeigen

```bash
python task_tool.py show 1
```

Task mit der ID 1 als erledigt markieren

```bash
python task_tool.py done 1
```

Alle Tasks anzeigen

```bash
python task_tool.py list
```

Nur erledigte Tasks anzeigen

```bash
python task_tool.py list --status done
```

Task mit der ID 1 löschen

```bash
python task_tool.py delete 1
```

## Bekannte Einschränkungen

- Keine Multi-User-Unterstützung
- Keine Synchronisation zwischen Geräten
- Daten werden lokal gespeichert