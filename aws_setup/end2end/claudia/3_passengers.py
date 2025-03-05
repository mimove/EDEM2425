from initial_info import passengers

for passenger in passengers:
    print(f"The passenger with name: {passenger['name']} is on the list")

count = len(passengers)
print(f"The total of passengers are: {count}")
