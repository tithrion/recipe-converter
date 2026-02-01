# Rezept-Konverter

Konvertiert Rezepte im Textformat in das schema.org/Recipe JSON-Format.

## Funktionen

- ✅ Konvertiert Textdateien in strukturierte JSON-Rezepte
- ✅ Erkennt automatisch Portionsangaben (z.B. "für 4 Personen")
- ✅ Erstellt separate Verzeichnisse für jedes Rezept
- ✅ Unterstützt schema.org/Recipe Standard
- ✅ Verarbeitet einzelne oder mehrere Dateien
- ✅ Bereinigt Verzeichnisnamen automatisch

## Installation

Keine zusätzlichen Abhängigkeiten erforderlich. Das Script verwendet nur Python Standard-Bibliotheken.

**Voraussetzungen:**
- Python 3.6 oder höher

## Verwendung

### Grundlegende Verwendung

```bash
python3 recipe_converter.py <Rezeptdatei.txt>
```

### Mehrere Dateien konvertieren

```bash
python3 recipe_converter.py rezept1.txt rezept2.txt rezept3.txt
```

### Alle Rezepte in einem Verzeichnis

```bash
python3 recipe_converter.py rezepte/
```

### Mit Wildcards

```bash
python3 recipe_converter.py rezepte/*.txt
```

### Eigenes Ausgabeverzeichnis

```bash
python3 recipe_converter.py rezept.txt --output meine_rezepte
```

## Format der Eingabedateien

Die Textdateien sollten folgendes Format haben:

```
Rezeptname [optional: für X Personen]
Zutaten:
- Menge Maßeinheit Zutat 1
- Menge Maßeinheit Zutat 2
- Zutat ohne Mengenangabe
Zubereitung:
- Anweisung 1
- Anweisung 2
- Anweisung 3
```

### Beispiel

```
Apfelkuchen für 4 Personen
Zutaten:
- 200 g Mehl
- 100 g Zucker
- 2 Stück Eier
- 100 ml Milch
- 3 große Äpfel
- Zimt nach Geschmack
Zubereitung:
- Mehl und Zucker vermischen
- Eier und Milch hinzufügen
- Teig in Form geben
- Bei 180°C 40 Minuten backen
```

## Ausgabeformat

Das Script erstellt für jedes Rezept:

1. Ein Unterverzeichnis mit dem Rezeptnamen (bereinigte Version)
2. Darin eine `recipe.json` im schema.org/Recipe Format

### Verzeichnisstruktur

```
converted/
├── Apfelkuchen/
│   └── recipe.json
├── Guacamole/
│   └── recipe.json
└── ...
```

### JSON-Struktur

```json
{
  "id": "",
  "name": "Apfelkuchen",
  "description": "",
  "url": "",
  "image": "",
  "prepTime": null,
  "cookTime": null,
  "totalTime": null,
  "recipeCategory": "",
  "keywords": "",
  "recipeYield": 4,
  "tool": [],
  "recipeIngredient": [
    "200 g Mehl",
    "100 g Zucker",
    "2 Stück Eier"
  ],
  "recipeInstructions": [
    "- Mehl und Zucker vermischen",
    "- Eier und Milch hinzufügen"
  ],
  "nutrition": {
    "@type": "NutritionInformation"
  },
  "@context": "http://schema.org",
  "@type": "Recipe",
  "dateCreated": "2026-02-01T14:28:12+00:00",
  "dateModified": "2026-02-01T14:28:12+00:00",
  "datePublished": null,
  "printImage": true,
  "imageUrl": ""
}
```

## Besondere Funktionen

### Automatische Portionserkennung

Das Script erkennt automatisch Portionsangaben in verschiedenen Formaten:
- "für 4 Personen"
- "4 Personen"
- "4 Portionen"
- "ergibt 6 Portionen"

Diese werden aus dem Namen extrahiert und in `recipeYield` gespeichert.

### Verzeichnisname-Bereinigung

Sonderzeichen, die in Dateinamen nicht erlaubt sind, werden automatisch durch Unterstriche ersetzt:
- `< > : " / \ | ? *` → `_`

### Flexible Zutatenformate

Das Script akzeptiert Zutaten mit oder ohne Mengenangaben:
- ✅ `200 g Mehl`
- ✅ `2 Stück Eier`
- ✅ `Salz nach Geschmack`

## Fehlerbehandlung

Das Script gibt informative Fehlermeldungen aus und zeigt am Ende eine Zusammenfassung:

```
============================================================
Konvertierung abgeschlossen:
  Erfolgreich: 8
  Fehler: 0
  Ausgabeverzeichnis: /home/user/converted
============================================================
```

## Tipps

1. **Portionsangaben**: Platzieren Sie diese im Rezeptnamen (z.B. "Lasagne für 6 Personen") oder in der ersten Zutat
2. **Leerzeilen**: Diese werden automatisch ignoriert
3. **Bindestrich**: Können bei Zutaten und Anweisungen verwendet werden oder weggelassen werden
4. **Encoding**: Dateien sollten UTF-8 kodiert sein für korrekte Umlaute

## Disclaimer

Keine Garantie für korrekte und fehlerfreie Funktion. Backups sind grundsätzlich Pflicht.

## Lizenz

Dieses Script ist frei verfügbar unter der GPL v3.
