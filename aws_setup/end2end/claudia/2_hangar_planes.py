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

for airplane in airplanes:
    print(f"The airplane with plate number {airplane['plateNumber']} is in Hangar {airplane['hangarId']}")

count = len(airplanes)
print(f"The total of airplanes are: {count}")