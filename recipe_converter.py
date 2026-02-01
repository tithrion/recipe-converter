#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recipe Converter: Converts text files to schema.org/Recipe JSON format
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def extract_servings(text: str) -> tuple[str, Optional[int]]:
    """
    Extracts serving information from text.
    
    Args:
        text: Text that may contain serving information
        
    Returns:
        Tuple of (cleaned text, number of servings)
    """
    # Patterns for German serving information
    patterns = [
        r'für\s+(\d+)\s+Person(?:en)?',
        r'(\d+)\s+Person(?:en)?',
        r'(\d+)\s+Portion(?:en)?',
        r'ergibt\s+(\d+)\s+Portion(?:en)?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            servings = int(match.group(1))
            # Remove serving information from text
            cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
            return cleaned_text, servings
    
    return text, None


def parse_recipe_file(filepath: Path) -> Dict:
    """
    Parses a recipe text file and extracts information.
    
    Args:
        filepath: Path to the recipe text file
        
    Returns:
        Dictionary with extracted recipe data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Initialize variables
    recipe_name = ""
    ingredients = []
    instructions = []
    servings = 1
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        # First non-empty line is the recipe name
        if not recipe_name and not line.lower().startswith(('zutaten:', 'zubereitung:')):
            recipe_name = line
            # Check if serving information in name
            recipe_name, extracted_servings = extract_servings(recipe_name)
            if extracted_servings:
                servings = extracted_servings
            continue
        
        # Recognize sections (German keywords)
        if line.lower().startswith('zutaten:'):
            current_section = 'ingredients'
            continue
        elif line.lower().startswith('zubereitung:'):
            current_section = 'instructions'
            continue
        
        # Add content to current section
        if current_section == 'ingredients':
            # Remove leading dashes and spaces
            ingredient = line.lstrip('- ').strip()
            if ingredient:
                # Check if serving information in ingredient
                ingredient, extracted_servings = extract_servings(ingredient)
                if extracted_servings:
                    servings = extracted_servings
                ingredients.append(ingredient)
        
        elif current_section == 'instructions':
            # Keep dashes for instructions
            instruction = line.strip()
            if instruction:
                instructions.append(instruction)
    
    # Create recipe.json structure
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    # Create directory name (clean special characters)
    dir_name = re.sub(r'[<>:"/\\|?*]', '_', recipe_name)
    dir_name = dir_name.strip('. ')
    
    recipe_data = {
        "id": "",
        "name": recipe_name,
        "description": "",
        "url": "",
        "image": "",
        "prepTime": None,
        "cookTime": None,
        "totalTime": None,
        "recipeCategory": "",
        "keywords": "",
        "recipeYield": servings,
        "tool": [],
        "recipeIngredient": ingredients,
        "recipeInstructions": instructions,
        "nutrition": {
            "@type": "NutritionInformation"
        },
        "@context": "http://schema.org",
        "@type": "Recipe",
        "dateCreated": date_str,
        "dateModified": date_str,
        "datePublished": None,
        "printImage": True,
        "imageUrl": ""
    }
    
    return {
        "recipe": recipe_data,
        "dir_name": dir_name
    }


def convert_recipes(input_paths: List[str], output_dir: str = "converted"):
    """
    Converts recipe text files to JSON format.
    
    Args:
        input_paths: List of paths to text files or directories
        output_dir: Output directory (default: "converted")
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Collect all text files
    files_to_process = []
    for input_path in input_paths:
        path = Path(input_path)
        
        if path.is_file() and path.suffix.lower() in ['.txt', '.text']:
            files_to_process.append(path)
        elif path.is_dir():
            # Find all .txt files in directory
            files_to_process.extend(path.glob('*.txt'))
            files_to_process.extend(path.glob('*.text'))
        else:
            print(f"Warnung: '{input_path}' ist keine gültige Datei oder Verzeichnis")
    
    if not files_to_process:
        print("Keine Textdateien zum Konvertieren gefunden.")
        return
    
    print(f"Verarbeite {len(files_to_process)} Rezept(e)...\n")
    
    # Process each file
    success_count = 0
    error_count = 0
    
    for filepath in files_to_process:
        try:
            print(f"Konvertiere: {filepath.name}")
            
            # Parse recipe
            result = parse_recipe_file(filepath)
            recipe_data = result["recipe"]
            dir_name = result["dir_name"]
            
            # Create recipe directory
            recipe_dir = output_path / dir_name
            recipe_dir.mkdir(exist_ok=True)
            
            # Save recipe.json
            json_path = recipe_dir / "recipe.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(recipe_data, f, ensure_ascii=False, indent=2)
            
            print(f"  ✓ Erstellt: {recipe_dir}/recipe.json")
            print(f"    - Name: {recipe_data['name']}")
            print(f"    - Zutaten: {len(recipe_data['recipeIngredient'])}")
            print(f"    - Anweisungen: {len(recipe_data['recipeInstructions'])}")
            print(f"    - Portionen: {recipe_data['recipeYield']}")
            print()
            
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Fehler bei {filepath.name}: {str(e)}\n")
            error_count += 1
    
    # Summary
    print("=" * 60)
    print(f"Konvertierung abgeschlossen:")
    print(f"  Erfolgreich: {success_count}")
    print(f"  Fehler: {error_count}")
    print(f"  Ausgabeverzeichnis: {output_path.absolute()}")
    print("=" * 60)


def main():
    """Main function with command line support"""
    if len(sys.argv) < 2:
        print("Rezept-Konverter")
        print("=" * 60)
        print("Verwendung:")
        print(f"  {sys.argv[0]} <Datei1.txt> [Datei2.txt ...] [--output DIR]")
        print(f"  {sys.argv[0]} <Verzeichnis> [--output DIR]")
        print()
        print("Beispiele:")
        print(f"  {sys.argv[0]} rezept.txt")
        print(f"  {sys.argv[0]} rezepte/*.txt")
        print(f"  {sys.argv[0]} rezepte/ --output meine_rezepte")
        print()
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    output_dir = "converted"
    input_paths = []
    
    i = 0
    while i < len(args):
        if args[i] == '--output' and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        else:
            input_paths.append(args[i])
            i += 1
    
    if not input_paths:
        print("Fehler: Keine Eingabedateien angegeben")
        sys.exit(1)
    
    # Convert recipes
    convert_recipes(input_paths, output_dir)


if __name__ == "__main__":
    main()
