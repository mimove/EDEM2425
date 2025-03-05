from initial_info import airplanes

def get_airplanes_in_hangars(airplanes):
    return [plane for plane in airplanes if "hangarId" in plane]

airplanes_in_hangars = get_airplanes_in_hangars(airplanes)
for plane in airplanes_in_hangars:
    print(f"Airplane {plane['plateNumber']} ({plane['type']}) is in hangar {plane['hangarId']}")