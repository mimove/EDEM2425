from initial_info import passengers, flights
import pandas as pd

passengers_df = pd.DataFrame(passengers)

arrived_passenger_ids = []
for flight in flights:
    if "arrivalTime" in flight and flight["arrivalTime"]:  # Solo vuelos que han aterrizado
        arrived_passenger_ids.extend([pid for pid, status in flight["passengerIds"] if status == "Boarded"])

arrived_passengers_df = passengers_df[passengers_df["passengerId"].isin(arrived_passenger_ids)]

print(arrived_passengers_df)



