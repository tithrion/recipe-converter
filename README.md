# Recipe Converter

Converts recipes in text format to schema.org/Recipe JSON format.

## Features

- ✅ Converts text files to structured JSON recipes
- ✅ Automatically detects serving information (e.g., "für 4 Personen")
- ✅ Creates separate directories for each recipe
- ✅ Supports schema.org/Recipe standard
- ✅ Processes single or multiple files
- ✅ Automatically cleans directory names

## Installation

No additional dependencies required. The script uses only Python standard libraries.

**Requirements:**
- Python 3.6 or higher

## Usage

### Basic Usage

```bash
python3 recipe_converter.py <recipe_file.txt>
```

### Convert Multiple Files

```bash
python3 recipe_converter.py rezept1.txt rezept2.txt rezept3.txt
```

### All Recipes in a Directory

```bash
python3 recipe_converter.py rezepte/
```

### With Wildcards

```bash
python3 recipe_converter.py rezepte/*.txt
```

### Custom Output Directory

```bash
python3 recipe_converter.py rezept.txt --output meine_rezepte
```

## Input File Format

The text files should have the following format (in German):

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

### Example

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

## Output Format

The script creates for each recipe:

1. A subdirectory with the recipe name (cleaned version)
2. A `recipe.json` file in schema.org/Recipe format

### Directory Structure

```
converted/
├── Apfelkuchen/
│   └── recipe.json
├── Guacamole/
│   └── recipe.json
└── ...
```

### JSON Structure

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

## Special Features

### Automatic Serving Detection

The script automatically recognizes serving information in various German formats:
- "für 4 Personen"
- "4 Personen"
- "4 Portionen"
- "ergibt 6 Portionen"

These are extracted from the name and stored in `recipeYield`.

### Directory Name Cleaning

Special characters not allowed in file names are automatically replaced with underscores:
- `< > : " / \ | ? *` → `_`

### Flexible Ingredient Formats

The script accepts ingredients with or without quantity specifications:
- ✅ `200 g Mehl`
- ✅ `2 Stück Eier`
- ✅ `Salz nach Geschmack`

## Error Handling

The script provides informative error messages and shows a summary at the end:

```
============================================================
Konvertierung abgeschlossen:
  Erfolgreich: 8
  Fehler: 0
  Ausgabeverzeichnis: /home/user/converted
============================================================
```

## Tips

1. **Serving information**: Place this in the recipe name (e.g., "Lasagne für 6 Personen") or in the first ingredient
2. **Empty lines**: These are automatically ignored
3. **Dashes**: Can be used with ingredients and instructions or omitted
4. **Encoding**: Files should be UTF-8 encoded for correct umlauts

## License

This script is freely available for use and modification.
