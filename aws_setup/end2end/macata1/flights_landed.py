import os
import sys
from datetime import datetime
import pytz

def check_flight_status():
    try:
        # Add the directory containing the file to Python path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Dynamically import the initial_info module
        import initial_info
        
        # Get the current time in UTC
        current_time = datetime.now(pytz.UTC)
        
        # Check each flight in the list
        for flight in initial_info.flights:
            # Parse the times and ensure they are UTC
            departure_time = datetime.fromisoformat(flight['departureTime']).replace(tzinfo=pytz.UTC)
            arrival_time = datetime.fromisoformat(flight['arrivalTime']).replace(tzinfo=pytz.UTC)
            
            # Check if flight has landed (current time is past arrival time)
            if current_time > arrival_time:
                print(f"Landed Flight Details:")
                print(f"  Flight ID: {flight['flightId']}")
                print(f"  Plate Number: {flight['plateNumber']}")
                print(f"  Origin: {flight['origin']}")
                print(f"  Destination: {flight['destination']}")
                print(f"  Departure Time: {departure_time}")
                print(f"  Arrival Time: {arrival_time}")
                print(f"  Occupied Seats: {flight['occupiedSeats']}")
                print()  # Empty line for readability
    
    except ImportError:
        print("Error: Could not import initial_info. Please ensure the file exists and is named 'initial_info.py'.")
    except KeyError as e:
        print(f"Error: Missing required flight information - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_flight_status()