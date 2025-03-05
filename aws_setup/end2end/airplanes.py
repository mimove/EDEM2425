from initial_info import airplanes
import pandas as pd


airplanes_df = pd.DataFrame(airplanes)

airplanes_in_hangars_df = airplanes_df[["plateNumber", "type", "hangarId", "ownerName"]]

print(airplanes_in_hangars_df)

registered_airplanes_df = airplanes_df[["plateNumber", "type", "hangarId", "ownerName", 
                                        "lastMaintenanceDate", "nextMaintenanceDate", 
                                        "capacity", "fuel_capacity"]]

print(registered_airplanes_df)
