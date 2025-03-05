passengers = [
                {
                    "passengerId": "P-1001",
                    "name": "Ana García Martínez",
                    "nationalId": "12345678A",
                    "dateOfBirth": "1991-05-15",
                },
                {
                    "passengerId": "P-1002",
                    "name": "Carlos Rodríguez López",
                    "nationalId": "87654321B",
                    "dateOfBirth": "1973-11-30",
                },
                {
                    "passengerId": "P-1003",
                    "name": "Elena Sánchez García",
                    "nationalId": "11223344C",
                    "dateOfBirth": "1988-03-25",
                },
                {
                    "passengerId": "P-1004",
                    "name": "Javier Martínez Pérez",
                    "nationalId": "44332211D",
                    "dateOfBirth": "1995-07-10",
                },
                {
                    "passengerId": "P-1005",
                    "name": "María López Rodríguez",
                    "nationalId": "33441122E",
                    "dateOfBirth": "1985-09-05",
                },
                {
                    "passengerId": "P-1006",
                    "name": "Pedro García Sánchez",
                    "nationalId": "22114433F",
                    "dateOfBirth": "1979-01-20",
                },
                {
                    "passengerId": "P-1007",
                    "name": "Sara Pérez Martínez",
                    "nationalId": "55443322G",
                    "dateOfBirth": "1999-12-15",
                },
                {
                    "passengerId": "P-1008",
                    "name": "Juan Sánchez López",
                    "nationalId": "66554433H",
                    "dateOfBirth": "1977-08-25",
                },
                {
                    "passengerId": "P-1009",
                    "name": "Lucía Martínez García",
                    "nationalId": "77665544I",
                    "dateOfBirth": "1990-02-10",
                },
                {
                    "passengerId": "P-1010",
                    "name": "Antonio García López",
                    "nationalId": "88776655J",
                    "dateOfBirth": "1980-06-05",
                },
                {
                    "passengerId": "P-1011",
                    "name": "Beatriz López Sánchez",
                    "nationalId": "99887766K",
                    "dateOfBirth": "1983-04-30",
                },
                {
                    "passengerId": "P-1012",
                    "name": "Carmen Martínez Rodríguez",
                    "nationalId": "11001122L",
                    "dateOfBirth": "1975-10-15",
                },
                {
                    "passengerId": "P-1013",
                    "name": "David Sánchez Martínez",
                    "nationalId": "22110033M",
                    "dateOfBirth": "1987-03-20",
                },
                {
                    "passengerId": "P-1014",
                    "name": "Elena García López",
                    "nationalId": "33221100N",
                    "dateOfBirth": "1978-07-25",
                },
                {
                    "passengerId": "P-1015",
                    "name": "Fernando López Martínez",
                    "nationalId": "44332211O",
                    "dateOfBirth": "1982-01-10",
                },
                {
                    "passengerId": "P-1016",
                    "name": "Gloria Martínez Sánchez",
                    "nationalId": "55443322P",
                    "dateOfBirth": "1984-09-05",
                },
                {
                    "passengerId": "P-1017",
                    "name": "Hugo Sánchez García",
                    "nationalId": "66554433Q",
                    "dateOfBirth": "1986-02-20",
                },
                {   
                    "passengerId": "P-1018",
                    "name": "Isabel García López",
                    "nationalId": "77665544R",
                    "dateOfBirth": "1976-12-15",
                },
                {
                    "passengerId": "P-1019",
                    "name": "Javier López Martínez",
                    "nationalId": "88776655S",
                    "dateOfBirth": "1981-08-25",
                },
                {
                    "passengerId": "P-1020",
                    "name": "Karla Martínez García",
                    "nationalId": "99887766T",
                    "dateOfBirth": "1989-02-10",
                }
            ]

for passenger in passengers:
    print(f"The passenger with name: {passenger['name']} is on the list")

count = len(passengers)
print(f"The total of passengers are: {count}")