import random
import json

documents = ["device_request_queries.txt", "network_queries.txt", "password_reset.txt", "profile_setup.txt", "hardware_queries.txt" ]
default_scenarios = ["greetings.txt", "apreciations.txt", "goodbyes.txt"]
mask_lists = [ "softwares.txt", "devices.txt", "areas.txt", "networks.txt"]
dir_root = "./documents/"


def _get_doc_lines(path):
    with open(path, 'r') as f:
        doc_lines = f.readlines();
    lines = []
    for line in doc_lines:
        lines.append(line.replace("\n", ""))
    return lines;

def _fetch_intent_patterns(path):
    with open(path, 'r') as f:
        doc_lines = f.readlines();

    intents = []
    for line in doc_lines:
        line = line.replace("\n", "")
        line = line.replace("?", " ?")
        line = line.replace(",", " ,")
        line = line.replace(".", " .")

        intent = {}
        intent["words"] = line.split(" ")
        intents.append(intent)

    return intents

patterns = {
        "requests": _fetch_intent_patterns(dir_root + documents[0]),
        "network":  _fetch_intent_patterns(dir_root + documents[1]),
        "password": _fetch_intent_patterns(dir_root + documents[2]),
        "profile": _fetch_intent_patterns(dir_root + documents[3]),
        "hardware": _fetch_intent_patterns(dir_root + documents[4]),
        "greeting": _fetch_intent_patterns(dir_root + default_scenarios[0]),
        "apreciation": _fetch_intent_patterns(dir_root + default_scenarios[1]),
        "goodbye": _fetch_intent_patterns(dir_root + default_scenarios[2]),
        }

pattern_switcher = {i: pattern_type for i, pattern_type in enumerate(patterns.keys())}

masks = {
        "softwares" : _get_doc_lines(dir_root + mask_lists[0]),
        "devices" : _get_doc_lines(dir_root + mask_lists[1]),
        "areas" : _get_doc_lines(dir_root + mask_lists[2]),
        "networks" : _get_doc_lines(dir_root + mask_lists[3]),
        }

mask_switcher = { "1": "softwares", "3": "devices", "5": "areas", "7": "networks"}

def _generate_random_intent():
    scenario_label = random_int(0, 4)
    pattern_scenario = pattern_switcher.get(scenario_label, "requests")
    pattern_list = patterns[pattern_scenario]
    pattern = pattern_list[random_int(0, len(pattern_list) -1)]
    
    ner_tags = []
    words = []
    for word in pattern["words"]:
        if word in mask_switcher:
            mask_list = masks[mask_switcher[word]]
            mask = mask_list[random_int(0, len(mask_list) -1 )]
            mask = mask.split(" ")
            words.extend(mask)
            label = int(word)
            ner_tags.extend(label for _ in mask)
        else:
            words.append(word)
            ner_tags.append(0)
    
    intent = {
            "intent": pattern_scenario,
            "intent_label": scenario_label,
            "words": words,
            "ner_tags": ner_tags
            }
    return intent

def random_int(min_value, max_value):
    return random.randint(min_value, max_value)

def _get_random_default():
    scenario_label = random_int(5, 7)
    pattern_scenario = pattern_switcher.get(scenario_label, "greeting")
    pattern_list = patterns[pattern_scenario]
    pattern = pattern_list[random_int(0, len(pattern_list) -1)]

    intent = {
            "intent": pattern_scenario,
            "intent_label": scenario_label,
            "words": pattern["words"],
            "ner_tags": [0 for _ in pattern["words"]]
            }
    return intent



def _generate_dataset(size, defaults=0.2):
    dataset = {
            "labels": ["O", "B-SOFTWARE", "I-SOFTWARE", "B-DEVICE", "I-DEVICE", "B-AREA", "I-AREA", "B-NETWORK", "I-NETWORK" ] ,
            "label_tags": [0, 1, 2, 3, 4, 5, 6, 7, 8 ],
            "scenarios": ["request", "network", "password", "profile", "hardware", "greeting", "appreciation", "goodbye"],
            "scenario_tags": [0, 1, 2, 3, 4, 5, 6, 7 ],
            }

    defaults_limit = size * defaults
    addedDefaults = 0
    tagged_intents = []
    for _ in range(0, size):
        if random_int(0, 10) >= (defaults * 10) or addedDefaults >= defaults_limit:
            tagged_intents.append(_generate_random_intent())
        else:
            tagged_intents.append(_get_random_default())
            addedDefaults = addedDefaults + 1

    dataset["intents"] = tagged_intents
    dataset["size"] = len(tagged_intents)

    return dataset

data = _generate_dataset(100)

with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

