# Updated Data
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
        "passengerIds": [
            [
                "P-1001",
                "Boarded"
            ],
            [
                "P-1002",
                "Boarded"
            ],
            [
                "P-1003",
                "Boarded"
            ],
            [
                "P-1004",
                "Boarded"
            ],
            [
                "P-1005",
                "Boarded"
            ],
            [
                "P-1006",
                "Boarded"
            ]
        ]
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
        "passengerIds": [
            [
                "P-1010",
                "Boarded"
            ],
            [
                "P-1011",
                "Boarded"
            ],
            [
                "P-1012",
                "Cancelled"
            ],
            [
                "P-1013",
                "Boarded"
            ],
            [
                "P-1014",
                "Boarded"
            ],
            [
                "P-1015",
                "Boarded"
            ],
            [
                "P-1016",
                "Boarded"
            ],
            [
                "P-1017",
                "Cancelled"
            ]
        ]
    }
]
passengers = [
    {
        "passengerId": "P-1001",
        "name": "Ana Garc\u00eda Mart\u00ednez",
        "nationalId": "12345678A",
        "dateOfBirth": "1991-05-15"
    },
    {
        "passengerId": "P-1002",
        "name": "Carlos Rodr\u00edguez L\u00f3pez",
        "nationalId": "87654321B",
        "dateOfBirth": "1973-11-30"
    },
    {
        "passengerId": "P-1003",
        "name": "Elena S\u00e1nchez Garc\u00eda",
        "nationalId": "11223344C",
        "dateOfBirth": "1988-03-25"
    },
    {
        "passengerId": "P-1004",
        "name": "Javier Mart\u00ednez P\u00e9rez",
        "nationalId": "44332211D",
        "dateOfBirth": "1995-07-10"
    },
    {
        "passengerId": "P-1005",
        "name": "Mar\u00eda L\u00f3pez Rodr\u00edguez",
        "nationalId": "33441122E",
        "dateOfBirth": "1985-09-05"
    },
    {
        "passengerId": "P-1006",
        "name": "Pedro Garc\u00eda S\u00e1nchez",
        "nationalId": "22114433F",
        "dateOfBirth": "1979-01-20"
    },
    {
        "passengerId": "P-1007",
        "name": "Sara P\u00e9rez Mart\u00ednez",
        "nationalId": "55443322G",
        "dateOfBirth": "1999-12-15"
    },
    {
        "passengerId": "P-1008",
        "name": "Juan S\u00e1nchez L\u00f3pez",
        "nationalId": "66554433H",
        "dateOfBirth": "1977-08-25"
    },
    {
        "passengerId": "P-1009",
        "name": "Luc\u00eda Mart\u00ednez Garc\u00eda",
        "nationalId": "77665544I",
        "dateOfBirth": "1990-02-10"
    },
    {
        "passengerId": "P-1010",
        "name": "Antonio Garc\u00eda L\u00f3pez",
        "nationalId": "88776655J",
        "dateOfBirth": "1980-06-05"
    },
    {
        "passengerId": "P-1011",
        "name": "Beatriz L\u00f3pez S\u00e1nchez",
        "nationalId": "99887766K",
        "dateOfBirth": "1983-04-30"
    },
    {
        "passengerId": "P-1012",
        "name": "Carmen Mart\u00ednez Rodr\u00edguez",
        "nationalId": "11001122L",
        "dateOfBirth": "1975-10-15"
    },
    {
        "passengerId": "P-1013",
        "name": "David S\u00e1nchez Mart\u00ednez",
        "nationalId": "22110033M",
        "dateOfBirth": "1987-03-20"
    },
    {
        "passengerId": "P-1014",
        "name": "Elena Garc\u00eda L\u00f3pez",
        "nationalId": "33221100N",
        "dateOfBirth": "1978-07-25"
    },
    {
        "passengerId": "P-1015",
        "name": "Fernando L\u00f3pez Mart\u00ednez",
        "nationalId": "44332211O",
        "dateOfBirth": "1982-01-10"
    },
    {
        "passengerId": "P-1016",
        "name": "Gloria Mart\u00ednez S\u00e1nchez",
        "nationalId": "55443322P",
        "dateOfBirth": "1984-09-05"
    },
    {
        "passengerId": "P-1017",
        "name": "Hugo S\u00e1nchez Garc\u00eda",
        "nationalId": "66554433Q",
        "dateOfBirth": "1986-02-20"
    },
    {
        "passengerId": "P-1018",
        "name": "Isabel Garc\u00eda L\u00f3pez",
        "nationalId": "77665544R",
        "dateOfBirth": "1976-12-15"
    },
    {
        "passengerId": "P-1019",
        "name": "Javier L\u00f3pez Mart\u00ednez",
        "nationalId": "88776655S",
        "dateOfBirth": "1981-08-25"
    },
    {
        "passengerId": "P-1020",
        "name": "Karla Mart\u00ednez Garc\u00eda",
        "nationalId": "99887766T",
        "dateOfBirth": "1989-02-10"
    }
]
