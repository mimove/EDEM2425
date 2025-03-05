import initial_info

print("Planes in the hangar:")
for plane in initial_info.airplanes:
    print(f"  Plate Number: {plane['plateNumber']}")
    print(f"  Model: {plane['type']}")
    print(f"  Capacity: {plane['capacity']}")
    print(f"  ownerID: {plane['ownerId']}")
    print(f"  hangarID: {plane['hangarId']}")
    print()  # Empty line for readability
