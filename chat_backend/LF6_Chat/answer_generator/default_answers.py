import random

default_scenarios = ["greetings.txt", "apreciations.txt", "goodbyes.txt", "unknown.txt"]
dir_root = "./patterns/"

def _fetch_lines(path):
    with open(path, 'r') as f:
        doc_lines = f.readlines();
    patterns = []
    for line in doc_lines:
        patterns.append(line.replace("\n", ""))
    return patterns


patterns = {
        "GREETING": _fetch_lines(dir_root + default_scenarios[0]),
        "APRECIATION": _fetch_lines(dir_root + default_scenarios[1]),
        "GOODBYE": _fetch_lines(dir_root + default_scenarios[2]),
        "UNKNOWN": _fetch_lines(dir_root + default_scenarios[3]),
        }

def get_pattern(label):
    pattern_list = patterns[label]
    return pattern_list[random.randint(0, len(pattern_list) - 1)]

