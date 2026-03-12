# CLI-Tasks - Branch: `main-ki-serialize`

> **Hinweis:** Dieser Branch ist ein Forschungsartefakt und stellt nicht den finalen Code-Stand des Projekts dar.

## Kontext

Dieser Branch dokumentiert den Entwicklungsstand nach den Tasks 9-11 (Phase 3 - Implementierung Kernfunktion) im Rahmen der zugehörigen Bachelorarbeit.

Im Zuge von Task 9 ("Task erstellen", KI-Bedingung) hat das KI-System (Claude) im generierten Code bereits eine vollständige JSON-Serialisierungslogik (`serialize.py`) implementiert - obwohl dieser Teil explizit **nicht** zum Scope von Task 9 gehörte. Die KI hat damit die Anforderung von Task 12 ("JSON-Speicherung") vorweggenommen.

Da Task 12 als **Ohne-KI-Aufgabe** definiert war, hätte eine direkte Übernahme der KI-generierten `serialize.py` die Studienbedingung verfälscht. Deshalb wurde `serialize.py` in Task 12 auf einem separaten Branch vollständig manuell neu implementiert.

**Dieser Branch endet daher bei Task 11.**

## Abgrenzung

| Branch | Inhalt | Bedingung |
|---|---|---|
| `main-ki-serialize` | Tasks 9–11, `serialize.py` KI-generiert | Zwischenstand |
| `main` | Finaler Code-Stand nach Task 18 (Refactoring) | Abgabestand |

## Bachelorarbeit

*Die Auswirkungen von Künstlicher Intelligenz auf den Softwareentwicklungsprozess - Eine empirische Untersuchung zur Zusammenarbeit zwischen Mensch und KI*
