'''
Takes as input a csv file in the form:
name,class,start,num
(e.g.: IMU, C, 5, 19)

And creates a list of stickers and their colours in the form 
text, colour,
IMU-C5, blue, 
...
IMU-C19, blue,

This csv forms the input to the create_stickers.py file.
'''

import csv



# CONSTANTS
input_csv = "stickers-input.csv"      # Your input file
output_csv = "stickers.csv"    # Your generated file

colour_map = {
    "IMU": "blue",
    "GPS": "blue",
    "ANM": "blue",
    "MAX": "blue",
    "PCB": "green",
    "BAT": "green",
    "THR": "green",
    "SOL": "green",
    "RDM": "red",
    "SLM": "red",
    "SAI": "red",
    "RUD": "red",
    "DPN": "yellow",
    "HTC": "yellow",
    "SPN": "yellow",
    "BPN": "yellow",
}

# === Processing ===
rows = []

with open(input_csv, newline='') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        name_base = row['name']
        cls = row['class']
        start = int(row['start'])
        end = start + int(row['num'])

        colour = colour_map.get(name_base, "black")  # default to 'black' if not found

        for i in range(start, end):
            full_name = f"{name_base}-{cls}{i}"
            rows.append({"text": full_name, "colour": colour})

# === Output ===
with open(output_csv, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['text', 'colour'])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows in '{output_csv}'.")
