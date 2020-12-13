import csv
import json


def to_csv(data, filepath, fieldnames=None):
    """Write data to CSV file"""
    print(f'Writing test data to {filepath}')
    with open(f'{filepath}', 'w', newline='') as file:
        if fieldnames is None:
            fieldnames = data[0].keys()
        dict_writer = csv.DictWriter(file, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def to_json(data, filepath):
    """Write data to JSON file"""
    print(f'Writing test data to {filepath}')
    with open(f'{filepath}', 'w') as file:
        json.dump(data, file)


def json_objects_to_str(data, filepath):
    """Write JSON objects as strings"""
    print(f'Writing test data to {filepath}')
    with open(f'{filepath}', 'w') as file:
        for d in data:
            file.write(json.dumps(d) + '\n')
