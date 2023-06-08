import json
import os
from fuzzywuzzy import fuzz

def get_answer(label, entities):
    path = f"scenario_handler/{label_map[label]}"
    data = handler_map[label](path, entities)
    return data

def load_routine(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return json_data
    else:
        print(f"JSON file  does not exist in the '{file_path}' folder.")
        return None


def handle_request(path, entities):
    request_url = _generate_hardware_request_url(entities['DEVICE'], entities['AREA'])
    return {"answer": f"Um eine Bestellung für Hardware aufzugeben, folgen Sie dem folgenden Link, um das Bestellformular auszufüllen und abzuschicken: {request_url}"}

def _generate_hardware_request_url(device_names, division_names):
    base_url = "www.it-solutions.com/hardware_request"

    if not device_names and not division_names:
        return base_url

    encoded_devices = [name.replace(" ", "%20") for name in device_names]
    devices_param = "&devices=" + "%20".join(encoded_devices)
    encoded_divisions = [name.replace(" ", "%20") for name in division_names]
    divisions_param = "&divisions=" + "%20".join(encoded_divisions)

    hardware_request_url = base_url + "?" + devices_param + divisions_param

    return hardware_request_url

def handle_network(path, entities):
    full_path = f"{path}/internet_routine.json"
    return load_routine(full_path)


def handle_password(path, entities):
    try:
        software = entities['SOFTWARE'][0]
    except:
        software = ''
    file_name = find_matching_file(path, software)
    if file_name:
        return load_routine(f"{path}/{file_name}")
    else: 
        return {"answer": "Ich konnte keine Informationen über dieses System finden, aber die Software-Abteilung wird Ihnen gerne helfen, rufen Sie xxx xxx xxx xxx an oder senden Sie eine E-Mail an software_support@it_solutions.com und sie werden Ihr Passwort zurücksetzen."}

def handle_profile(path, entities):
    try:
        software = entities['SOFTWARE'][0]
    except:
        software = ''
    file_name = find_matching_file(path, software)
    if file_name:
        return load_routine(f"{path}/{file_name}")
    else: 
        return {"answer": "Ich konnte keine Informationen zu diesem System finden, aber die Software-Abteilung hilft Ihnen gerne weiter. Rufen Sie xxx xxx xxx xxx an oder schicken Sie eine E-Mail an software_support@it_solutions.com und sie helfen Ihnen gerne weiter."}

def handle_hardware(path, entities):
    try:
        device = entities['DEVICE'][0]
    except:
        device = ''
    file_name = find_matching_file(path, device)
    if file_name:
        return load_routine(f"{path}/{file_name}")
    else: 
        return {"answer": "Es tut mir leid, dass ich Ihnen nicht helfen kann, aber die Infrastrukturabteilung wird Ihnen gerne helfen, rufen Sie xxx xxx xxx an oder schreiben Sie eine E-Mail an infrastructure_and_hardware@it_solutions.com und sie werden Ihnen sofort helfen."}

handler_map = {
        "REQUEST": handle_request,
        "NETWORK": handle_network,
        "PASSWORD": handle_password,
        "PROFILE": handle_profile,
        "HARDWARE": handle_hardware
        }

label_map = {
     "REQUEST": "request_routines",
     "NETWORK": "network_routines",
     "PASSWORD": "password_routines",
     "PROFILE": "profile_routines",
     "HARDWARE": "hardware_routines"
     }

def find_matching_file(path, search_string):
    matching_file = None
    max_similarity = 0
    print(search_string)

    if search_string == '':
        return None

    print(os.listdir(path))
    for file_name in os.listdir(path):
        if file_name.endswith(".json"):
            similarity = fuzz.ratio(file_name, search_string)
            if similarity > max_similarity:
                max_similarity = similarity
                matching_file = file_name
    return matching_file if matching_file else None
