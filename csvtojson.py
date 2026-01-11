import csv
import json
import os

def rename_file(old_name, new_name):
    try:
        # Check if the old file exists
        if not os.path.isfile(old_name):
            print(f"Error: File '{old_name}' does not exist.")
            return

        # Prevent overwriting an existing file
        if os.path.exists(new_name):
            print(f"Error: A file named '{new_name}' already exists.")
            return

        # Perform the rename
        os.rename(old_name, new_name)
        print(f"File renamed from '{old_name}' to '{new_name}' successfully.")

    except PermissionError:
        print("Error: Permission denied. Check file permissions.")
    except OSError as e:
        print(f"OS error occurred: {e}")


def m2():
    csv_file = "test.csv"
    json_file = "abc.json"

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)
    rename_file("abc.json", "response.json")



