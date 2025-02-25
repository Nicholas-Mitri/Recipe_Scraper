"""
Recipe PDF File Renamer

This script renames recipe PDF files in the 'recipe_pdfs' directory to a more readable format.
It extracts words from filenames, converts them to title case, and creates a new filename.

The script:
- Finds all PDF files in the recipe_pdfs directory
- Extracts words from each filename using regex
- Creates a new filename in Title Case format
- Renames the files with the new format
- Handles errors and provides feedback on the renaming process
"""

import re, glob, os
from pathlib import Path

# Get all PDF files in the recipe_pdfs directory
recipes = [recipe.split("/")[-1].lower() for recipe in glob.glob("recipe_pdfs/*.pdf")]
# Create a regex pattern to extract words from filenames
pattern = re.compile(r"\b[a-z]+\b")
# Get the current working directory
pwd = os.getcwd()
# Set the project path
recipes_path = os.path.join(pwd, "recipe_pdfs")
# Ensure the recipe_pdfs directory exists
os.makedirs(recipes_path, exist_ok=True)

# Process each recipe file
for recipe in recipes:
    # Extract words from the filename (excluding the last word which is likely "pdf")
    matches = pattern.findall(recipe)[:-1]

    # Create a new filename in Title Case format
    new_name = " ".join(matches).title() + ".pdf"
    print(new_name, recipe)
    try:
        # Check if a file with the new name already exists
        if os.path.exists(os.path.join(recipes_path, new_name)):
            print(f"Skipping: {new_name} already exists")
            continue
        # Rename the file
        os.rename(
            os.path.join(recipes_path, recipe), os.path.join(recipes_path, new_name)
        )
        print(f"Renamed: {recipe} → {new_name}")
    except Exception as e:
        # Handle any errors during renaming
        print(f"Error renaming {recipe}: {e}")
