from datetime import datetime
import csv
import logging
import os


import pytz
import requests


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()


class ValenciaHousePrice():
    def __init__(self, area_name):
        self.area_name = area_name
        self.parse_data_list = []

    @staticmethod
    def get_data_idealista_valencia(number_of_results=100):
        try:
            url = (
                f"https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
                f"precio-de-compra-en-idealista/records?limit={number_of_results}"
            )
            response = requests.get(url)
            logging.info("Getting response from Valencia Open Data")
            data = response.json()
            if data.get("error_code"):
                raise ValueError(f"Error in url: {data['message']}")
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return response.json()

    def parse_data(self, data):
        logging.info(f"Starting parsing of data for area(s): {self.area_name}")
        for raw_data in data["results"]:
            information_dict = {}
            information_dict["barrio"] = raw_data["barrio"]
            information_dict["distrito"] = raw_data["distrito"]
            information_dict["precio_2022_euros_m2"] = raw_data["precio_2022_euros_m2"]
            information_dict["precio_2010_euros_m2"] = raw_data["precio_2010_euros_m2"]
            information_dict["max_historico_euros_m2"] = raw_data["max_historico_euros_m2"]
            information_dict["ano_max_hist"] = raw_data["ano_max_hist"]
            information_dict["fecha_creacion"] = raw_data["fecha_creacion"]
            information_dict["requested_at"] = str(datetime.now(tz=pytz.utc).isoformat())
            if self.area_name == "all_areas":
                self.parse_data_list.append(information_dict)
            elif self.area_name == information_dict["barrio"]:
                self.parse_data_list.append(information_dict)
                logging.info("Parsing completed")
                return self.parse_data_list
        logging.info("Parsing completed")
        return self.parse_data_list

    def write_parse_data_list(self, area_name):
        logging.info("Starting writting of results...")
        file_path = "/project/"
        if not os.path.exists(file_path):
            logging.info(f"Creating path {file_path}")
            os.makedirs(file_path)
        file = file_path + f"{area_name}.csv"
        with open(file, 'w') as f:
            writer = csv.writer(f)
            csv_header = self.parse_data_list[0].keys()
            writer.writerow(csv_header)
            for area in self.parse_data_list:
                writer.writerow(area.values())
            logging.info("Finish writting")


if __name__ == "__main__":
    areas = "all_areas"
    valencia_data = ValenciaHousePrice(areas)
    data = valencia_data.get_data_idealista_valencia()
    parse_data_list = valencia_data.parse_data(data)
    valencia_data.write_parse_data_list(areas)
