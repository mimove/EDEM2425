import json
from initial_info import airplanes

def register_airplanes_from_file(airplanes, new_airplanes_file):
    try:
        with open(new_airplanes_file, "r") as file:
            new_airplanes = json.load(file)
            airplanes.extend(new_airplanes)
            save_airplanes(airplanes)
            print(f"{len(new_airplanes)} new airplanes have been registered.")
    except FileNotFoundError:
        print("New airplanes file not found.")

def save_airplanes(airplanes, filename="airplanes.json"):
    with open(filename, "w") as file:
        json.dump(airplanes, file, indent=4)

    
def load_airplanes(filename="airplanes.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    register_airplanes_from_file(airplanes, "new_airplanes.json")
