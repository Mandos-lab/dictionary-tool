import json
import os
import pdfplumber

# Path to your PDF file
PDF_FILENAME = "dictionary.pdf"
OUTPUT_DIR = "dist_dictionary"

os.makedirs(OUTPUT_DIR, exist_ok=True)

dictionary_data = []

print("Reading PDF file... This might take a few minutes for large files.")

# Step 1: Extract text from the PDF
with pdfplumber.open(PDF_FILENAME) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        if text:
            # Splits text into individual lines
            lines = text.split("\n")
            for line in lines:
                parts = line.strip().split(" ", 1)
                if len(parts) == 2:
                    word, definition = parts[0], parts[1]
                    dictionary_data.append({
                        "word": word,
                        "definition": definition,
                        "page": page_num
                    })

print(f"Extracted {len(dictionary_data)} entries. Grouping by letter...")

# Step 2: Separate entries by starting letter
buckets = {}
for entry in dictionary_data:
    first_char = entry["word"][0].upper()
    if first_char not in buckets:
        buckets[first_char] = []
    buckets[first_char].append(entry)

# Step 3: Save into JSON files and build index
index_manifest = {}
for letter, records in buckets.items():
    file_name = f"dictionary_{letter}.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        
    index_manifest[letter] = {
        "file": file_name,
        "count": len(records)
    }

with open(os.path.join(OUTPUT_DIR, "index.json"), "w", encoding="utf-8") as f:
    json.dump(index_manifest, f, ensure_ascii=False, indent=2)

print("Done! Check the 'dist_dictionary' folder in your project directory.")