import csv
import numpy as np

def read_data(filename):
    """Зчитує дані RPS та CPU з CSV файлу."""
    x = []
    y = []
    try:
        with open(filename, 'r', newline='') as file: #не обробляти символи переносу рядка
            reader = csv.DictReader(file) #DictReader зчитує перший рядок як ключ, решту як словник.
           #csv.reader просто витягнув би спиок
            for row in reader:
                x.append(float(row['RPS']))    #перетворення з рядка на число
                y.append(float(row['CPU']))
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
        return None, None
    return np.array(x), np.array(y)