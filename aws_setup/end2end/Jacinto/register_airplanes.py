import json
from datetime import datetime

class AircraftRegistry:
    def __init__(self, initial_aircraft=None):
        """
        Initialize the aircraft registry.
        
        :param initial_aircraft: Optional list of initial aircraft
        """
        self.aircraft_registry = initial_aircraft or []
        self.registry_file = 'aircraft_registry.json'
        self.load_registry()

    def load_registry(self):
        """
        Load existing aircraft registry from a JSON file.
        """
        try:
            with open(self.registry_file, 'r') as file:
                self.aircraft_registry = json.load(file)
        except FileNotFoundError:
            # If no file exists, start with an empty list
            self.aircraft_registry = []

    def save_registry(self):
        """
        Save the current aircraft registry to a JSON file.
        """
        with open(self.registry_file, 'w') as file:
            json.dump(self.aircraft_registry, file, indent=4)

    def register_aircraft(self, aircraft_details):
        """
        Register a new aircraft or update an existing one.
        
        :param aircraft_details: Dictionary containing aircraft information
        :return: Confirmation message
        """
        # Validate required fields
        required_fields = ['plateNumber', 'type', 'hangarId', 'ownerId', 'ownerName']
        for field in required_fields:
            if field not in aircraft_details:
                return f"Error: Missing required field '{field}'"

        # Check if aircraft already exists
        existing_aircraft = self.find_aircraft_by_plate(aircraft_details['plateNumber'])
        
        if existing_aircraft:
            # Update existing aircraft
            index = self.aircraft_registry.index(existing_aircraft)
            self.aircraft_registry[index] = {**existing_aircraft, **aircraft_details}
            action = "Updated"
        else:
            # Add registration timestamp for new aircraft
            aircraft_details['registrationDate'] = datetime.now().isoformat()
            self.aircraft_registry.append(aircraft_details)
            action = "Registered"

        # Save updated registry
        self.save_registry()
        
        return f"Aircraft {action}: {aircraft_details['plateNumber']} in Hangar {aircraft_details['hangarId']}"

    def find_aircraft_by_plate(self, plate_number):
        """
        Find an aircraft by its plate number.
        
        :param plate_number: Plate number of the aircraft
        :return: Aircraft details or None
        """
        return next(
            (aircraft for aircraft in self.aircraft_registry 
             if aircraft['plateNumber'] == plate_number), 
            None
        )

    def list_aircraft_in_hangar(self, hangar_id):
        """
        List all aircraft in a specific hangar.
        
        :param hangar_id: ID of the hangar
        :return: List of aircraft in the hangar
        """
        return [
            aircraft for aircraft in self.aircraft_registry 
            if aircraft['hangarId'] == hangar_id
        ]

    def display_aircraft_details(self, plate_number):
        """
        Display detailed information about a specific aircraft.
        
        :param plate_number: Plate number of the aircraft
        :return: Formatted aircraft details
        """
        aircraft = self.find_aircraft_by_plate(plate_number)
        
        if not aircraft:
            return f"No aircraft found with plate number {plate_number}"
        
        details = "Aircraft Details:\n"
        details += "=" * 30 + "\n"
        for key, value in aircraft.items():
            details += f"{key.replace('_', ' ').title()}: {value}\n"
        
        return details

def main():
    # Initialize the registry
    registry = AircraftRegistry()

    # Example usage demonstrating different functionalities
    while True:
        print("\n--- Aircraft Registration System ---")
        print("1. Register New Aircraft")
        print("2. Update Existing Aircraft")
        print("3. Find Aircraft by Plate Number")
        print("4. List Aircraft in a Hangar")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            # Collect aircraft details
            plate_number = input("Enter Plate Number: ")
            aircraft_type = input("Enter Aircraft Type: ")
            hangar_id = input("Enter Hangar ID: ")
            owner_id = input("Enter Owner ID: ")
            owner_name = input("Enter Owner Name: ")
            
            # Optional additional details
            capacity = input("Enter Passenger Capacity (optional): ") or None
            fuel_capacity = input("Enter Fuel Capacity (optional): ") or None
            
            # Prepare aircraft details
            aircraft_details = {
                'plateNumber': plate_number,
                'type': aircraft_type,
                'hangarId': hangar_id,
                'ownerId': owner_id,
                'ownerName': owner_name
            }
            
            # Add optional details if provided
            if capacity:
                aircraft_details['capacity'] = int(capacity)
            if fuel_capacity:
                aircraft_details['fuel_capacity'] = int(fuel_capacity)
            
            # Register aircraft
            result = registry.register_aircraft(aircraft_details)
            print(result)
        
        elif choice == '2':
            plate_number = input("Enter Plate Number to Update: ")
            aircraft = registry.find_aircraft_by_plate(plate_number)
            
            if aircraft:
                print("Current Details:")
                print(registry.display_aircraft_details(plate_number))
                
                # Collect update details
                hangar_id = input("Enter New Hangar ID (press Enter to skip): ") or aircraft['hangarId']
                owner_id = input("Enter New Owner ID (press Enter to skip): ") or aircraft['ownerId']
                owner_name = input("Enter New Owner Name (press Enter to skip): ") or aircraft['ownerName']
                
                update_details = {
                    'plateNumber': plate_number,
                    'hangarId': hangar_id,
                    'ownerId': owner_id,
                    'ownerName': owner_name
                }
                
                result = registry.register_aircraft(update_details)
                print(result)
            else:
                print(f"No aircraft found with plate number {plate_number}")
        
        elif choice == '3':
            plate_number = input("Enter Plate Number: ")
            print(registry.display_aircraft_details(plate_number))
        
        elif choice == '4':
            hangar_id = input("Enter Hangar ID: ")
            aircraft_in_hangar = registry.list_aircraft_in_hangar(hangar_id)
            
            if aircraft_in_hangar:
                print(f"\nAircraft in Hangar {hangar_id}:")
                for aircraft in aircraft_in_hangar:
                    print(f"- {aircraft['plateNumber']} ({aircraft['type']})")
            else:
                print(f"No aircraft found in Hangar {hangar_id}")
        
        elif choice == '5':
            print("Exiting Aircraft Registration System.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()