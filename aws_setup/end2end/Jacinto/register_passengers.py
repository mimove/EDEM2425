import json
from datetime import datetime

class PassengerRegistry:
    def __init__(self, filename='passengers.json'):
        """
        Initialize passenger registry.
        
        :param filename: File to store passenger data
        """
        self.filename = filename
        self.passengers = self._load_passengers()

    def _load_passengers(self):
        """
        Load existing passengers from JSON file.
        
        :return: List of passengers or empty list
        """
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_passengers(self):
        """
        Save passengers to JSON file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.passengers, file, indent=2)

    def register_passenger(self, passenger_details):
        """
        Register a new passenger or update existing passenger.
        
        :param passenger_details: Dictionary of passenger information
        :return: Registration confirmation message
        """
        # Validate required fields
        if not all(field in passenger_details for field in ['passengerId', 'name']):
            return "Error: Passenger ID and Name are required"

        # Check if passenger already exists
        existing_passenger = next(
            (p for p in self.passengers if p['passengerId'] == passenger_details['passengerId']), 
            None
        )

        if existing_passenger:
            # Update existing passenger
            existing_passenger.update(passenger_details)
            action = "Updated"
        else:
            # Add new passenger with registration timestamp
            passenger_details['registeredAt'] = datetime.now().isoformat()
            self.passengers.append(passenger_details)
            action = "Registered"

        # Save updated passenger list
        self._save_passengers()
        
        return f"Passenger {action}: {passenger_details['name']} (ID: {passenger_details['passengerId']})"

    def find_passenger(self, passenger_id):
        """
        Find a passenger by their ID.
        
        :param passenger_id: Passenger ID to search for
        :return: Passenger details or None
        """
        return next(
            (passenger for passenger in self.passengers 
             if passenger['passengerId'] == passenger_id), 
            None
        )

def main():
    registry = PassengerRegistry()

    while True:
        print("\n--- Passenger Registration System ---")
        print("1. Register Passenger")
        print("2. Find Passenger")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            # Collect passenger details
            passenger_details = {
                'passengerId': input("Passenger ID: "),
                'name': input("Full Name: "),
                'nationalId': input("National ID (optional): ") or None,
                'dateOfBirth': input("Date of Birth (YYYY-MM-DD, optional): ") or None,
                'flightId': input("Flight ID (optional): ") or None
            }
            
            # Remove None values
            passenger_details = {k: v for k, v in passenger_details.items() if v is not None}
            
            # Register passenger
            print(registry.register_passenger(passenger_details))

        elif choice == '2':
            passenger_id = input("Enter Passenger ID: ")
            passenger = registry.find_passenger(passenger_id)
            
            if passenger:
                print("\nPassenger Details:")
                for key, value in passenger.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
            else:
                print("Passenger not found")

        elif choice == '3':
            print("Exiting Passenger Registration System.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()