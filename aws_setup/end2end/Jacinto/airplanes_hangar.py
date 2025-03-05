# Airplane data directly in the script
airplanes = [
    {
        "plateNumber": "EC-XYZ1",
        "type": "Cessna 208 Caravan",
        "lastMaintenanceDate": "2024-04-15",
        "nextMaintenanceDate": "2025-04-15",
        "capacity": 9,
        "ownerId": "O-12345",
        "ownerName": "Madrid Flying Club",
        "hangarId": "H-01",
        "fuel_capacity": 700
    },
    {
        "plateNumber": "EC-ABC2",
        "type": "Piper PA-31 Navajo",
        "lastMaintenanceDate": "2025-02-10",
        "nextMaintenanceDate": "2027-02-10",
        "capacity": 7,
        "ownerId": "O-23456",
        "ownerName": "Catalina Aviation",
        "hangarId": "H-01",
        "fuel_capacity": 1000
    }
]

def get_hangar_aircraft(hangars_data):
    """
    Retrieve a list of aircraft currently stored in hangars.
    
    :param hangars_data: List of airplane dictionaries
    :return: Dictionary of hangars and their contained aircraft
    """
    # Group aircraft by hangar
    hangar_aircraft = {}
    
    for airplane in hangars_data:
        hangar_id = airplane['hangarId']
        
        # If hangar not yet in dictionary, create an empty list
        if hangar_id not in hangar_aircraft:
            hangar_aircraft[hangar_id] = []
        
        # Add airplane details to the hangar's list
        hangar_aircraft[hangar_id].append({
            'Plate Number': airplane['plateNumber'],
            'Aircraft Type': airplane['type'],
            'Owner': airplane['ownerName'],
            'Capacity': airplane['capacity'],
            'Last Maintenance': airplane['lastMaintenanceDate'],
            'Next Maintenance': airplane['nextMaintenanceDate']
        })
    
    return hangar_aircraft

def display_hangar_contents(hangar_aircraft):
    """
    Display detailed information about aircraft in each hangar.
    
    :param hangar_aircraft: Dictionary of hangars and their aircraft
    """
    if not hangar_aircraft:
        print("No aircraft are currently stored in hangars.")
        return
    
    print("Hangar Aircraft Inventory:")
    print("=" * 50)
    
    for hangar, aircraft_list in hangar_aircraft.items():
        print(f"\nHangar ID: {hangar}")
        print("-" * 30)
        
        if not aircraft_list:
            print("  No aircraft in this hangar.")
            continue
        
        for aircraft in aircraft_list:
            print(f"  Plate Number: {aircraft['Plate Number']}")
            print(f"  Aircraft Type: {aircraft['Aircraft Type']}")
            print(f"  Owner: {aircraft['Owner']}")
            print(f"  Passenger Capacity: {aircraft['Capacity']}")
            print(f"  Last Maintenance: {aircraft['Last Maintenance']}")
            print(f"  Next Maintenance: {aircraft['Next Maintenance']}")
            print("-" * 30)

def main():
    # Get aircraft by hangar
    hangar_aircraft = get_hangar_aircraft(airplanes)
    
    # Display hangar contents
    display_hangar_contents(hangar_aircraft)

if __name__ == "__main__":
    main()