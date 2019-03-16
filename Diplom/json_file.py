import json


def json_vkinder(json_data):
    with open("Vkinder v2.0.json", "w") as data_file:
        json.dump(json_data, data_file, indent=2)
