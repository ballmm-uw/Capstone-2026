import spacy
import pandas as pd
import json
import glob
import os  # Import os for folder operations

pd.options.display.max_rows = 600
pd.options.display.max_colwidth = 400

nlp = spacy.load('en_core_web_sm')

# Define file path and output folder
input_folder = r"C:\Users\GaliAlony\notepad++\individual_JSONs"
output_folder = os.path.join(input_folder, "processed_texts")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Debugging print
print("Loading JSON files...")

files = glob.glob(os.path.join(input_folder, "*.json"))

if not files:
    print("No JSON files found! Check your directory path.")
else:
    print(f"Found {len(files)} files.")

# Process each JSON file and save in the new folder
for filepath in files:
    filename = os.path.basename(filepath)  # Extracts filename from path
    output_file_path = os.path.join(output_folder, f"{filename}.txt")  # Save as .txt

    print(f"Processing {filepath}...")  # Debugging step

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        text = data.get('body', '')  # Ensure 'body' exists
        if not text:
            print(f"Warning: No 'body' found in {filepath}")

        document = nlp(text)

        with open(output_file_path, "w", encoding="utf-8") as out_file:
            for ent in document.ents:
                out_file.write(f"{ent.text}\t{ent.label_}\n")

        print(f"Saved output to {output_file_path}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"Processing complete. All outputs saved in {output_folder}.")