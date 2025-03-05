from datetime import datetime, timezone
from initial_info import flights

def get_arrived_passengers(flights):
    current_time = datetime.now(timezone.utc).isoformat()
    arrived_passengers = []
    
    for flight in flights:
        if flight["arrivalTime"] < current_time:
            arrived_passengers.extend([p[0] for p in flight["passengerIds"] if p[1] == 'Boarded'])
    
    return arrived_passengers

arrived_passengers = get_arrived_passengers(flights)
print("Passengers that have arrived:")
for passenger_id in arrived_passengers:
    print(passenger_id)