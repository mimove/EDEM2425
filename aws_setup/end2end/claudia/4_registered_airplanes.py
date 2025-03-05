from initial_info import airplanes

def register_airplane(plate_number):
    for airplane in airplanes:
        if airplane["plateNumber"] == plate_number:
            print(f"The airplane with plate number {airplane['plateNumber']} is a {airplane['type']} and is stored in Hangar {airplane['hangarId']}.")
            return
    print("Airplane not found.")


plate_number = input("Enter airplane plate number: ")
register_airplane(plate_number)
