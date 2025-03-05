flights = [
                {
                    "flightId": "FL-2025-001",
                    "plateNumber": "EC-XYZ1",
                    "arrivalTime": "2025-03-01T09:30:00",
                    "departureTime": "2025-03-01T14:45:00",
                    "fuelConsumption": 350,
                    "occupiedSeats": 7,
                    "origin": "Valencia",
                    "destination": "Paris",
                    "passengerIds": [("P-1001", 'Boarded'), ("P-1002", 'Boarded'), ("P-1003", 'Boarded'), ("P-1004", 'Boarded'), ("P-1005", 'Boarded'), ("P-1006", 'Boarded')]
                },
                {
                    "flightId": "FL-2025-002",
                    "plateNumber": "EC-ABC2",
                    "arrivalTime": "2025-03-02T11:15:00",
                    "departureTime": "2025-03-02T16:30:00",
                    "fuelConsumption": 850,
                    "occupiedSeats": 8,
                    "origin": "Barcelona",
                    "destination": "London",
                    "passengerIds": [("P-1010", 'Boarded'), ("P-1011", 'Boarded'), ("P-1012", 'Cancelled'), ("P-1013", 'Boarded'), ("P-1014", 'Boarded'), ("P-1015", 'Boarded'), ("P-1016", 'Boarded'), ("P-1017", 'Cancelled')]
                }
          ]

for flight in flights:
    print(f"The plane with plate number {flight['plateNumber']} has landed.")

count = len(flights)
print(f"The total of landed flights are: {count}")
