import csv
import json

SERIAL_NUMBER_COLUMN = '﻿Serial Number'

def convert_csv_to_json(csv_file, json_file):
    try:
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as csvfile, open(json_file, 'w') as jsonfile:
            reader = csv.DictReader(csvfile)
            data_list = []

            for row in reader:
                data = {key: value for key, value in row.items() if key != SERIAL_NUMBER_COLUMN}
                data_list.append(data)

            json.dump(data_list, jsonfile, indent=4)

    except FileNotFoundError:
        print(f"Error: The file {csv_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def add_indent_to_json_file(path):
    with open(path, 'r+') as f:
        json_data = json.load(f)
        f.seek(0)
        json.dump(json_data, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    convert_csv_to_json('csv_format/english_rules.csv', 'json_format/english_rules.json')
    convert_csv_to_json('csv_format/idioms_proverbs.csv', 'json_format/idioms_proverbs.json')
    add_indent_to_json_file("json_format/slang_expressions.json")