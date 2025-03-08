import json
from datetime import datetime
from initial_info import passengers

class PassengerRegistry:
    def __init__(self, initial_passengers):
        self.passengers = initial_passengers
        self.passenger_log = []
    
    def register_passenger_interactive(self):
        name = input("Ingrese el nombre completo del pasajero: ")
        national_id = input("Ingrese el número de identificación nacional: ")
        date_of_birth = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
        
        contact_info = {}
        add_contact = input("¿Desea agregar información de contacto? (s/n): ").lower()
        if add_contact == 's':
            while True:
                contact_type = input("Ingrese el tipo de contacto (email/phone/otro, o 'fin' para terminar): ").lower()
                if contact_type == 'fin':
                    break
                contact_value = input(f"Ingrese el {contact_type} del pasajero: ")
                contact_info[contact_type] = contact_value
        
        nationality = input("Ingrese la nacionalidad del pasajero (opcional, presione Enter para omitir): ")
        
        passenger = self.register_passenger(
            name=name, 
            national_id=national_id, 
            date_of_birth=date_of_birth,
            contact_info=contact_info if contact_info else None,
            nationality=nationality if nationality else None
        )
        
        print("\nPasajero registrado con éxito:")
        print(f"ID de Pasajero: {passenger['passengerId']}")
        print(f"Nombre: {passenger['name']}")
        
        return passenger
    
    def register_passenger(self, 
                            name, 
                            national_id, 
                            date_of_birth, 
                            contact_info=None, 
                            nationality=None):
        existing_passenger = next((p for p in self.passengers if p['nationalId'] == national_id), None)
        
        contact_details = contact_info or {}

        if not existing_passenger:
            passenger_id = str(len(self.passengers) + 1)
            new_passenger = {
                'passengerId': passenger_id,
                'name': name,
                'nationalId': national_id,
                'dateOfBirth': date_of_birth,
                'contactInfo': contact_details,
                'nationality': nationality,
                'registrationDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'visitHistory': []
            }
            self.passengers.append(new_passenger)
            passenger_info = new_passenger
        else:
            existing_passenger.update({
                'name': name,
                'dateOfBirth': date_of_birth,
                'contactInfo': contact_details,
                'nationality': nationality or existing_passenger.get('nationality')
            })
            passenger_info = existing_passenger

        arrival_log = {
            'passengerId': passenger_info['passengerId'],
            'arrivalTimestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': name,
            'flightInfo': self._get_recent_flight_info(name)
        }
        self.passenger_log.append(arrival_log)

        passenger_info['visitHistory'].append(arrival_log['arrivalTimestamp'])
        
        return passenger_info
    
    def _get_recent_flight_info(self, passenger_name):
        from initial_info import flights

        for flight in reversed(flights):
            for passenger_id, status in flight['passengerIds']:
                matching_passenger = next((p for p in passengers if 
                                           p['passengerId'] == passenger_id and 
                                           p['name'] == passenger_name), None)
                if matching_passenger:
                    return {
                        'flightId': flight['flightId'],
                        'origin': flight['origin'],
                        'destination': flight['destination'],
                        'departureTime': flight['departureTime'],
                        'arrivalTime': flight['arrivalTime']
                    }
        
        return None
    
    def search_passenger(self, search_term):
        return [
            passenger for passenger in self.passengers
            if (search_term.lower() in passenger['name'].lower() or
                search_term == passenger['nationalId'] or
                search_term == passenger['passengerId'])
        ]
    
    def generate_passenger_report(self):
        print("--- PASSENGER REGISTRY REPORT ---")
        for passenger in self.passengers:
            print("\nPassenger Details:")
            print(f"Passenger ID: {passenger['passengerId']}")
            print(f"Name: {passenger['name']}")
            print(f"National ID: {passenger['nationalId']}")
            print(f"Date of Birth: {passenger['dateOfBirth']}")
            
            if passenger.get('contactInfo'):
                print("Contact Information:")
                for key, value in passenger['contactInfo'].items():
                    print(f"  {key.capitalize()}: {value}")
            
            if passenger.get('nationality'):
                print(f"Nationality: {passenger['nationality']}")

            print(f"Registration Date: {passenger.get('registrationDate', 'N/A')}")
            print("Visit History:")
            if passenger.get('visitHistory'):
                for visit in passenger['visitHistory'][-5:]:  
                    print(f"  - {visit}")
            else:
                print("  No previous visits recorded")
    
    def save_passenger_registry(self, filename='passenger_registry.json'):
        with open(filename, 'w') as f:
            json.dump(self.passengers, f, indent=2)
        print(f"Passenger registry saved to {filename}")
    
    def save_passenger_log(self, filename='passenger_arrival_log.json'):
        with open(filename, 'w') as f:
            json.dump(self.passenger_log, f, indent=2)
        print(f"Passenger arrival log saved to {filename}")

def main():
    passenger_registry = PassengerRegistry(passengers)
    
    while True:
        print("\n--- REGISTRO DE PASAJEROS ---")
        print("1. Registrar nuevo pasajero")
        print("2. Generar informe de pasajeros")
        print("3. Buscar pasajero")
        print("4. Guardar registro de pasajeros")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            passenger_registry.register_passenger_interactive()
        elif opcion == '2':
            passenger_registry.generate_passenger_report()
        elif opcion == '3':
            search_term = input("Ingrese nombre, ID de pasajero o ID nacional para buscar: ")
            results = passenger_registry.search_passenger(search_term)
            if results:
                print("\nResultados de la búsqueda:")
                for passenger in results:
                    print(f"ID: {passenger['passengerId']}, Nombre: {passenger['name']}, ID Nacional: {passenger['nationalId']}")
            else:
                print("No se encontraron pasajeros.")
        elif opcion == '4':
            passenger_registry.save_passenger_registry()
            passenger_registry.save_passenger_log()
        elif opcion == '5':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()