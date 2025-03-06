from initial_info import airplanes
from datetime import datetime, date

def list_airplanes():
    for airplane in airplanes:
        print(f"Airplane {airplane['plateNumber']} is in hangar {airplane['hangarId']}: {airplane}")


def register_airplane():
    fields = {
        "plateNumber": "Introduce plate number: ",
        "type": "Introduce the type of the airplane: ",
        "lastMaintenanceDate": "Introduce the last maintenance date (YYYY-MM-DD): ",
        "nextMaintenanceDate": "Introduce the next maintenance date: ",
        "capacity": "Introduce the capacity: ",
        "ownerId": "Introduce the owner ID: ",
        "ownerName": "Introduce the owner name: ",
        "hangarId": "Introduce the hangar ID: ",
        "fuel_capacity": "Introduce the fuel capacity: "
    }
    new_airplane = {}

    for key, info in fields.items():
        value = info(info)
        if key in ["capacity", "fuel_capacity"]:
            value = float(value)
        new_airplane[key] = value
    
    airplanes.append(new_airplane)
    print('Airplane registered:', new_airplane)
    return new_airplane


def check_date():
    current_date = date.today()
    for airplane in airplanes:
        last_date = datetime.strptime(airplane["lastMaintenanceDate"], "%Y-%m-%d").date()
        next_date = datetime.strptime(airplane["nextMaintenanceDate"], "%Y-%m-%d").date()
        days_left = (next_date - current_date).days
        print(f"The next maintenance day for airplane {airplane["plateNumber"]} is in {days_left} days")

        if days_left < 100:
            print(f"ALERT: Airplane {airplane['plateNumber']} needs maintenance soon ({days_left} days left)! You should plan for the maintenance asap!")
        

if __name__ == "__main__":
    while True:
        print("\n1. List Airplanes")
        print("2. Register Airplane")
        print("3. Check Maintenance")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            list_airplanes()
        elif choice == "2":
            register_airplane()
        elif choice == "3":
            check_date()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")
        
        continue_actions = input("\nDo you want to do something else? (yes/no): ").strip().lower()
        if continue_actions == "no":
            print("Exiting program.")
            break