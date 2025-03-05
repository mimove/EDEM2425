from initial_info import airplanes

for airplane in airplanes:
    print(f"The airplane with plate number {airplane['plateNumber']} is in Hangar {airplane['hangarId']}")

count = len(airplanes)
print(f"The total of airplanes are: {count}")
