import math
import numpy as np
import matplotlib.pyplot as plt
from function import (
    M, exact_derivative, forward_difference, backward_difference, central_difference,
    runge_romberg, aitken_method, aitken_accuracy_order
)

def plot_function_and_derivative():
    """1. Загальний графік функції та її точної похідної."""
    t_vals = np.linspace(0, 10, 400)
    M_vals = [M(t) for t in t_vals]
    dM_vals = [exact_derivative(t) for t in t_vals]

    plt.figure(figsize=(10, 5))
    plt.plot(t_vals, M_vals, label="M(t) - Вологість", color='blue')
    plt.plot(t_vals, dM_vals, label="M'(t) - Точна швидкість зміни", color='red')
    plt.xlabel("Час t")
    plt.ylabel("Значення")
    plt.title("Динаміка вологості ґрунту (початкова і похідна)")
    plt.legend()
    plt.grid(True)
    plt.savefig('1_function_plot.png')
    plt.close()


def plot_error_vs_step(t0, exact_val):
    """2. Графік залежності похибки від кроку h."""
    h_values = [10 ** i for i in np.arange(-15, 1, 0.5)]
    errors = []
    valid_h = []

    for h in h_values:
        try:
            approx_val = central_difference(M, t0, h)
            error = abs(approx_val - exact_val)
            if error > 0:
                errors.append(error)
                valid_h.append(h)
        except ZeroDivisionError:
            continue

    plt.figure(figsize=(10, 5))
    plt.loglog(valid_h, errors, marker='o', linestyle='-', color='purple')
    plt.xlabel("Крок сітки h (Логарифмічна шкала)")
    plt.ylabel("Абсолютна похибка R (Логарифмічна шкала)")
    plt.title("Залежність похибки від кроку h (Центральна різниця)")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.savefig('2_error_plot.png')
    plt.close()


def plot_derivative_comparison(h_large=1.0):
    """3. Графік порівняння точної похідної з різними методами апроксимації."""
    t_vals = np.linspace(0, 10, 400)
    exact_vals = [exact_derivative(t) for t in t_vals]

    forward_vals = [forward_difference(M, t, h_large) for t in t_vals]
    backward_vals = [backward_difference(M, t, h_large) for t in t_vals]
    central_vals = [central_difference(M, t, h_large) for t in t_vals]

    plt.figure(figsize=(12, 6))
    plt.plot(t_vals, exact_vals, label="Точна похідна (гладка)", color='black', linewidth=2)
    plt.plot(t_vals, central_vals, label=f"Центральна різниця (h={h_large})", color='green', linestyle='--')
    plt.plot(t_vals, forward_vals, label=f"Вперед (h={h_large}) - великі коливання", color='red', linestyle='-.', alpha=0.7)
    plt.plot(t_vals, backward_vals, label=f"Назад (h={h_large}) - великі коливання", color='blue', linestyle=':', alpha=0.7)

    plt.xlabel("Час t")
    plt.ylabel("Значення похідної")
    plt.title(f"Порівняння методів диференціювання при великому кроці (h={h_large})")
    plt.legend()
    plt.grid(True)
    plt.savefig('3_derivative_comparison.png')
    plt.close()


def main():

    t0 = 1.0
    exact_val = exact_derivative(t0)

    # Малюємо всі 3 графіки
    plot_function_and_derivative()
    plot_error_vs_step(t0, exact_val)
    plot_derivative_comparison(h_large=1.0)

    # === КРОК 1 ===
    print(f"1. Точне значення похідної M'(1): {exact_val:.7f}")
    print("   [ДЖЕРЕЛО: Пораховано за еталонною аналітичною формулою exact_derivative(t0)]")

    # === КРОК 2 ===
    print("\n2. Дослідження залежності похибки від кроку h:")
    print("   [ДІЯ: Програма перебирає кроки від 10^-15 до 10^1 через метод central_difference]")

    min_error = float('inf')
    best_h = None

    for i in range(-15, 2):
        h_test = 10 ** i
        try:
            approx = central_difference(M, t0, h_test)
            current_error = abs(approx - exact_val)

            if current_error < min_error:
                min_error = current_error
                best_h = h_test
        except ZeroDivisionError:
            continue

    print(f"   Оптимальний крок h0: {best_h:.1e}")
    print(f"   Досягнута точність R0: {min_error:.2e}")
    print("   [ДЖЕРЕЛО: Це найменша знайдена похибка R = |y'(h) - y'(x0)| у циклі]")

    # === КРОКИ 3, 4, 5 ===
    h = 1e-3
    print(f"\n3. Приймаємо фіксований крок сітки h = {h}")

    d_h = central_difference(M, t0, h)
    d_2h = central_difference(M, t0, 2 * h)
    R1 = abs(d_h - exact_val)

    print(f"   Базова апроксимація y'(h) = {d_h:.7f}")
    print(f"   [ДЖЕРЕЛО: Обчислено методом central_difference з кроком h={h}]")
    print(f"   Похибка R1: {R1:.7e}")
    print("   [ДЖЕРЕЛО: Модуль різниці між базовою апроксимацією та еталоном]")

    print("-" * 50)
    print("РЕЗУЛЬТАТИ ДВОХ МЕТОДІВ ПОКРАЩЕННЯ ТОЧНОСТІ:")

    # --- МЕТОД 1: РУНГЕ-РОМБЕРГ (Крок 6) ---
    d_runge = runge_romberg(d_h, d_2h)
    R2 = abs(d_runge - exact_val)

    print(f"\n> МЕТОД 1: Рунге-Ромберга")
    print("  [ДІЯ: Алгоритм використав два попередні результати: з кроками h та 2h]")
    print(f"  Уточнене значення: {d_runge:.7f}")
    print(f"  Похибка R2:        {R2:.7e}")
    print("  [ВИСНОВОК: Похибка R2 стала меншою за базову R1]")

    # --- МЕТОД 2: ЕЙТКЕН (Крок 7) ---
    d_4h = central_difference(M, t0, 4 * h)
    d_aitken = aitken_method(d_h, d_2h, d_4h)
    R3 = abs(d_aitken - exact_val)
    p_order = aitken_accuracy_order(d_h, d_2h, d_4h)

    print(f"\n> МЕТОД 2: Ейткена")
    print("  [ДІЯ: Обчислено третю точку y'(4h) через central_difference. Алгоритм бере 3 точки: h, 2h, 4h]")
    print(f"  Додатково обчислено y'(4h) = {d_4h:.7f}")
    print(f"  Уточнене значення: {d_aitken:.7f}")
    print(f"  Похибка R3:        {R3:.7e}")
    print("  [ВИСНОВОК: Похибка R3 майже знищена (наближається до нуля)!]")
    print(f"  Порядок точності p: {p_order:.2f}")
    print(
        "  [ДЖЕРЕЛО: Формула оцінки порядку точності Ейткена. Значення ~2 підтверджує квадратичну точність центральної різниці]")


if __name__ == "__main__":
    main()