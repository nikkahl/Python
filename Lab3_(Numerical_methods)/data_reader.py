import csv

def read_data(filename="data.csv"):
    x, y = [], []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    return x, y