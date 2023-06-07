import json
import os

label_map = {
     "REQUEST": "request_routines",
     "NETWORK": "network_routines",
     "PASSWORD": "password_routines",
     "PROFILE": "profile_routines",
     "HARDWARE": "hardware_routines"
     }

def get_answer(label, entities):
    path = f"scenario_handler/{label_map[label]}/internet_routine.json"
    data = load_routine(path)
    if data:
        return data
    else:
        return {"answer": "not found"}

def load_routine(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return json_data
    else:
        print(f"JSON file  does not exist in the '{file_path}' folder.")
        return None
