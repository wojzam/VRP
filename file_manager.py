import csv

from customers import Point, Customer, CustomerPair


def write_customers_to_file(customers, column_names, file):
    rows = [customer.get_coordinates() for customer in customers]
    with open(file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
        csvwriter.writerows(rows)


def read_customers_from_file(file):
    customers = []
    with open(file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            customers.append(retrieve_customer(row))
    return customers


def retrieve_customer(row):
    row = list(map(int, row))
    try:
        return Customer(Point(*row))
    except TypeError:
        return CustomerPair(Point(row[0], row[1]), Point(row[2], row[3]))
