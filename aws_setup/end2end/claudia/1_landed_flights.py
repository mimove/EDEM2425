from initial_info import flights

for flight in flights:
    print(f"The plane with plate number {flight['plateNumber']} has landed.")

count = len(flights)
print(f"The total of landed flights are: {count}")
