from initial_info import airplanes, passengers, flights
from datetime import datetime
import json

def get_airplanes():
    return airplanes 

def detail_airplanes(airplanes):
    print("Airplanes Jacinto, vuela seguro")
    print(f"Numero de aviones disponibles en estos momentos: {len(airplanes)}")
    
    for airplane in airplanes:
        print(f"Airplane numero {airplanes.index(airplane) +1}")
        print(f"Plate Number: {airplane['plateNumber']}")

if __name__ == '__main__':
    detail_airplanes(airplanes)