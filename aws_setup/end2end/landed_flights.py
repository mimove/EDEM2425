from datetime import datetime, timezone
from initial_info import flights

def get_landed_flights(flights):
    current_time = datetime.now(timezone.utc).isoformat()  # Usando datetime con timezone UTC
    
    landed_flights = [flight for flight in flights if flight["arrivalTime"] < current_time]
    
    return landed_flights

landed_flights = get_landed_flights(flights)
for flight in landed_flights:
    print(f"Flight {flight['flightId']} from {flight['origin']} to {flight['destination']} has landed.")