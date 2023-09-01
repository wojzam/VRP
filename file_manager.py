import csv

from delivery_request import DeliveryRequest

DEFAULT_FILENAME = "requests.csv"


def write_requests_to_file(requests, filename=DEFAULT_FILENAME):
    rows = [request.get_coordinates() for request in requests]
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['startX', 'startY', 'endX', 'endY'])
        csvwriter.writerows(rows)


def read_requests_from_file(filename=DEFAULT_FILENAME):
    rows = []
    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            rows.append(row)

    return [DeliveryRequest(*map(float, row)) for row in rows]
