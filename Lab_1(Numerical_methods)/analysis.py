import numpy as np


def analyze_route(distances: np.ndarray, elevations: np.ndarray, mass: float = 80.0):
    """
    Аналізує характеристики маршруту, включаючи набір висоти та механічну роботу.
    """
    total_distance = distances[-1]

    n = len(elevations)
    total_ascent = sum(max(elevations[i] - elevations[i - 1], 0) for i in range(1, n))
    total_descent = sum(max(elevations[i - 1] - elevations[i], 0) for i in range(1, n))

    # Механічна енергія підйому
    g = 9.81
    energy_joules = mass * g * total_ascent
    energy_kcal = energy_joules / 4184

    # Аналіз градієнта
    grad_full = np.gradient(elevations, distances) * 100

    print("\n--- Додатковий Аналіз Маршруту ---")
    print(f"Загальна довжина маршруту: {total_distance:.2f} м")
    print(f"Сумарний набір висоти: {total_ascent:.2f} м")
    print(f"Сумарний спуск: {total_descent:.2f} м")
    print(f"Максимальний підйом (%): {np.max(grad_full):.2f}")
    print(f"Максимальний спуск (%): {np.min(grad_full):.2f}")
    print(f"Середній градієнт (%): {np.mean(np.abs(grad_full)):.2f}")
    print(f"Механічна робота: {energy_joules:.2f} Дж ({energy_joules / 1000:.2f} кДж)")
    print(f"Витрачена енергія: {energy_kcal:.2f} ккал")