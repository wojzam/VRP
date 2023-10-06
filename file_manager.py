import csv

from customer_pair import CustomerPair

DEFAULT_FILENAME = "customers.py"


def write_customers_to_file(customers, filename=DEFAULT_FILENAME):
    rows = [customer.get_coordinates() for customer in customers]
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['startX', 'startY', 'endX', 'endY'])
        csvwriter.writerows(rows)


def read_customers_from_file(filename=DEFAULT_FILENAME):
    rows = []
    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            rows.append(row)

    return [CustomerPair(*map(float, row)) for row in rows]
