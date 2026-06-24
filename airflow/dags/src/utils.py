from pathlib import Path

def get_query_str_from_file(file_path: str | Path) -> str:

    # Open the file in read mode and extract its contents into a string variable
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()