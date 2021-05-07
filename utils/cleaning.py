import re


def clean_string(string: str) -> str:
    string = "".join(line for line in string.splitlines() if line)
    string = re.sub(' +', ' ', string)
    return string
