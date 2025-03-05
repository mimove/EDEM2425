from initial_info import flights
import pandas as pd

for flight in flights:
    if "passengerIds" in flight:
        flight["passengerIds"] = [[pid, status] for pid, status in flight["passengerIds"]]

landed_flights = [
    {
        "flightId": flight["flightId"],
        "plateNumber": flight["plateNumber"],
        "arrivalTime": flight["arrivalTime"],
        "origin": flight["origin"],
        "destination": flight["destination"],
    }
    for flight in flights if "arrivalTime" in flight and flight["arrivalTime"]
]

landed_flights_df = pd.DataFrame(landed_flights)

print(landed_flights_df)

flights_aerodrome_df = pd.DataFrame(flights)

landed_flights_on_aerodrome_df = flights_aerodrome_df[["flightId", "plateNumber", "arrivalTime", "origin", "destination"]]


