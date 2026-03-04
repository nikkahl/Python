import numpy as np
import matplotlib.pyplot as plt
from api_client import fetch_elevation_data
from geo_utils import calculate_haversine
from spline_math import calculate_spline_coefficients, evaluate_spline
from analysis import analyze_route


def main():
    url = ("https://api.open-elevation.com/api/v1/lookup?locations="
           "48.164214,24.536044|48.164983,24.534836|48.165605,24.534068|"
           "48.166228,24.532915|48.166777,24.531927|48.167326,24.530884|"
           "48.167011,24.530061|48.166053,24.528039|48.166655,24.526064|"
           "48.166497,24.523574|48.166128,24.520214|48.165416,24.517170|"
           "48.164546,24.514640|48.163412,24.512980|48.162331,24.511715|"
           "48.162015,24.509462|48.162147,24.506932|48.161751,24.504244|"
           "48.161197,24.501793|48.160580,24.500537|48.160250,24.500106")

    print("Виконуємо запит до API...")
    results = fetch_elevation_data(url)

    coords = [(p["latitude"], p["longitude"]) for p in results]  #на виході координати широти, довжини, х
    elevations = np.array([p["elevation"] for p in results])  #тут підйом y

    # 3. Обчислюємо кумулятивну відстань
    n_points = len(results)   #21
    distances = np.zeros(n_points)   #масив 21 нулів    ініціалізація пам'яті
    for i in range(1, n_points):   #номер точки, другі дужки 0 чи 1 (широта чи довгота)
        d = calculate_haversine(coords[i - 1][0], coords[i - 1][1], coords[i][0], coords[i][1]) #0-широта 1-довгота, довжина кроку
#перевели координати в метри, записали в масив
        distances[i] = distances[i - 1] + d #кумулятивна відстань для подальшої побудови

    # 4. Записуємо вхідні дані в файл
    with open("output.txt", "w") as f:
        f.write("Index | Distance (m) | Elevation (m)\n")
        f.write("-" * 40 + "\n")
        for i in range(n_points):
            f.write(f"{i:2d}    | {distances[i]:10.2f} | {elevations[i]:10.2f}\n")  #2 - ширина поля; кумулятивна відстань флот+ширина поля +точність

    print("Табуляцію вузлів збережено у файл output.txt")

    # гладкий профіль маршруту (Еталон) для першого графіка, більша кількість точок
    a_full, b_full, c_full, d_full = calculate_spline_coefficients(distances, elevations) #передаємо Х  та У в функцію spline, повертає 4 масиви коефіцієнтів для кожної точки
    x_smooth_profile = np.linspace(distances.min(), distances.max(), 1000) # 0 - 3060 / 1000
    y_smooth_profile = evaluate_spline(x_smooth_profile, distances, a_full, b_full, c_full, d_full) # підстановка в класичне рівняння кубічного сплайна еталонних даних

    for i in range(len(a_full)):
        print(f"Коефіцієнт {i:2d} | {a_full[i]:16.2f} | {b_full[i]:15.6f} | {c_full[i]:15.6e} | {d_full[i]:18.6e}")

    node_counts = [10, 15, 20]

    plt.figure(figsize=(10, 6))   #ширина вікна,так сказав чат джпт
    plt.plot(x_smooth_profile, y_smooth_profile, label="21 вузол (еталон)", linewidth=2) #робим більшу ширину

    errors_smooth = {} #словник ключ значення (набір точок : масив 1000 значень похибки для кожного вузла)

    for count in node_counts:
        # Вибираємо вузли рівномірно
        indices = np.linspace(0, n_points - 1, count, dtype=int)   #linspace рівномірно обираєм 10-15-20 вузлів серед  усіх
        # 21 на вирахування похибки, по іншому 0-10 то обчислення закінчувались б на середині гори.) [0, 2, 4, 6, 8, 11, 13, 15, 17, 20] для 10

        x_subset = distances[indices]  #дякуєм numpy ( витягуємо значення з х та у)
        y_subset = elevations[indices]

        a, b, c, d = calculate_spline_coefficients(x_subset, y_subset)
        y_smooth_approx = evaluate_spline(x_smooth_profile, x_subset, a, b, c, d)

        epsilon_smooth = np.abs(y_smooth_profile - y_smooth_approx)  #похибка, віднімаємо два масиви по 1000 точок
        errors_smooth[f"{count} вузлів"] = epsilon_smooth    #1000 похибок в словник

        print(f"\n--- {count} вузлів ---")
        print(f"Максимальна похибка: {np.max(epsilon_smooth):.4f}")
        print(f"Середня похибка: {np.mean(epsilon_smooth):.4f}")

        plt.plot(x_smooth_profile, y_smooth_approx, label=f"{count} вузлів")

    plt.title("Вплив кількості вузлів на інтерполяцію")
    plt.xlabel("Кумулятивна відстань (м)")
    plt.ylabel("Висота (м)")
    plt.legend()
    plt.grid(True)


    plt.figure(figsize=(10, 6))
    for label, eps_smooth in errors_smooth.items():  # items - дістає елементи парами
        # без маркерів, щоб лінії були плавними
        plt.plot(x_smooth_profile, eps_smooth, label=label)

    plt.title("Похибка апроксимації ε = |y - y_approx|")
    plt.xlabel("Кумулятивна відстань (м)")
    plt.ylabel("Похибка (м)")
    plt.legend()
    plt.grid(True)

    # Виводимо аналіз у консоль
    analyze_route(distances, elevations)

    print("\nМалюємо графіки...")
    plt.show()


if __name__ == "__main__":
    main()