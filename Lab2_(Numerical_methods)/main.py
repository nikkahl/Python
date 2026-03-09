import numpy as np
import matplotlib.pyplot as plt
from data_handler import read_data
from interpolation import (divided_differences, newton_polynomial,
                           forward_differences, factorial_polynomial, test_function)


def main():
    x_data, y_data = read_data("data.csv")

    if x_data is None:
        return

    print("-" * 60)
    print("Вхідні дані (RPS -> CPU):")
    for i in range(len(x_data)):
        print(f"Відсоток використання CPU при RPS {x_data[i]}: {y_data[i]}%")

    # 2. Обчислення Ньютона
    newton_coefs = divided_differences(x_data, y_data) #математична таблиця розділених різниць
    rps_target = 600
    cpu_newton = newton_polynomial(x_data, newton_coefs, rps_target)

    # 3. Обчислення Факторіального многочлена
    diffs = forward_differences(y_data) # різниці
    t_indices = np.arange(len(x_data))  # cтворення масиву РІВОМІРОГО для формули у мене від 0 до 5
    t_target = np.interp(rps_target, x_data, t_indices)  #викик лінійної інтерполяції -> число (перевод rps в дробовий індекс)
    #interp приймає три аргументи 1- шуканий , решту відомі. Шукаємо індекс для 600 rps
    cpu_factorial = factorial_polynomial(diffs, t_target) #int -> відсоток CPU

    print("-" * 60)
    print(f"Відсоток використання CPU при RPS {rps_target} (многочлен Ньютона): {cpu_newton}%")
    print(f"Відсоток використання CPU при RPS {rps_target} (факторіальний многочлен): {cpu_factorial}%")
    print("-" * 60)


    plot_graphs(x_data, y_data, newton_coefs, diffs, t_indices, rps_target, cpu_newton)

def plot_graphs(x_data, y_data, newton_coefs, diffs, t_indices, rps_target, cpu_newton):
    plt.style.use('bmh')  # тема графіка
    fig, axes = plt.subplots(3, 2, figsize=(16, 10))
    fig.canvas.manager.set_window_title('Лаб2 - варіант2')

    # 1. Графік Ньютона (Верхній лівий)
    x_dense = np.linspace(min(x_data), max(x_data), 200)
    y_newton_dense = [newton_polynomial(x_data, newton_coefs, x) for x in x_dense]

    axes[0, 0].plot(x_dense, y_newton_dense, 'r-', linewidth=2, label='Інтерполяційний многочлен Ньютона')
    axes[0, 0].scatter(x_data, y_data, color='navy', zorder=5, label='Дані точки')
    axes[0, 0].scatter([rps_target], [cpu_newton], color='green', marker='*', s=150, zorder=6,
                       label=f'Прогноз (RPS={rps_target})')
    axes[0, 0].set_title("Інтерполяційний многочлен Ньютона", fontsize=12)
    axes[0, 0].set_xlabel("Запити за секунду")
    axes[0, 0].set_ylabel("Використання CPU")
    axes[0, 0].legend(loc='upper left')

    # 2. Графік факторіальних многочленів (Верхній правий)
    t_dense = np.linspace(0, max(t_indices), 200)
    x_mapped = np.interp(t_dense, t_indices, x_data)

    axes[0, 1].scatter(x_data, y_data, color='black', zorder=5, label='Дані точки')
    colors = ['orange', 'yellow', 'green', 'cyan']

    for k in range(1, len(diffs)):
        y_fact_k = [factorial_polynomial(diffs[:k + 1], t) for t in t_dense]
        axes[0, 1].plot(x_mapped, y_fact_k, color=colors[k - 1], linestyle='--', linewidth=2, alpha=0.9,
                        label=f'Інтерпольовані точки (порядок {k})')

    axes[0, 1].set_title("Факторіальні многочлени", fontsize=12)
    axes[0, 1].set_xlabel("Запити за секунду")
    axes[0, 1].set_ylabel("Використання CPU")
    axes[0, 1].legend(loc='upper left')


    x_runge_dense = np.linspace(0, 1, 500)
    y_runge_true = test_function(x_runge_dense)
    nodes_list = [5, 10, 20]

    node_colors = ['red', 'orange', 'gold']

    # напівпрозорість (alpha=0.3)
    # Кладемо на самий низ (zorder=1)
    axes[1, 0].plot(x_runge_dense, y_runge_true, color='black', linewidth=6, alpha=0.3, label='Справжня функція',
                    zorder=1)
    axes[2, 0].plot(x_runge_dense, y_runge_true, color='black', linewidth=6, alpha=0.3, label='Справжня функція',
                    zorder=1)

    for i, n in enumerate(nodes_list):
        x_nodes = np.linspace(0, 1, n)
        y_nodes = test_function(x_nodes)

        # -------------------------------------------
        # Ньютон (Дослідження)
        # -------------------------------------------
        coefs = divided_differences(x_nodes, y_nodes)
        y_interp = [newton_polynomial(x_nodes, coefs, x) for x in x_runge_dense]

        error = np.abs(y_runge_true - np.array(y_interp))
        error_safe = np.maximum(error, 1e-16)  # Запобігаємо помилці логарифма від 0

        # Тонші кольорові лінії поверх чорної (zorder=i+2 гарантує правильне накладання)
        axes[1, 0].plot(x_runge_dense, y_interp, color=node_colors[i], linewidth=2, label=f'{n} точок', zorder=i + 2)
        axes[1, 1].plot(x_runge_dense, error_safe, color=node_colors[i], linewidth=2, label=f'Похибка ({n} точок)',
                        zorder=i + 2)

        # -------------------------------------------
        # Факторіальний (Дослідження)
        # -------------------------------------------
        diffs_runge = forward_differences(y_nodes)
        t_nodes_runge = np.arange(n)
        y_interp_fact = []
        for x in x_runge_dense:
            t_val = np.interp(x, x_nodes, t_nodes_runge)
            y_interp_fact.append(factorial_polynomial(diffs_runge, t_val))

        error_fact = np.abs(y_runge_true - np.array(y_interp_fact))
        error_fact_safe = np.maximum(error_fact, 1e-16)  # Запобігаємо помилці логарифма від 0

        # Тонші кольорові лінії поверх чорної
        axes[2, 0].plot(x_runge_dense, y_interp_fact, color=node_colors[i], linewidth=2, label=f'{n} точок',
                        zorder=i + 2)
        axes[2, 1].plot(x_runge_dense, error_fact_safe, color=node_colors[i], linewidth=2, label=f'Похибка ({n} точок)',
                        zorder=i + 2)

    # Налаштування підписів
    axes[1, 0].set_title("Інтерполяційні многочлени Ньютона", fontsize=10)
    axes[1, 0].set_xlabel("Запити за секунду (нормалізовані)")
    axes[1, 0].set_ylabel("Використання CPU")
    axes[1, 0].legend(loc='upper right')

    axes[1, 1].set_title("Похибки інтерполяційних многочленів Ньютона (Логарифмічна шкала)", fontsize=10)
    axes[1, 1].set_xlabel("Запити за секунду (нормалізовані)")
    axes[1, 1].set_ylabel("Похибка (лог)")
    axes[1, 1].set_yscale('log')  # Вмикаємо логарифмічну шкалу
    axes[1, 1].set_ylim(1e-17, 1)  # Фіксуємо рамки, щоб виглядало красиво
    axes[1, 1].legend(loc='lower center')

    axes[2, 0].set_title("Факторіальні многочлени", fontsize=10)
    axes[2, 0].set_xlabel("Запити за секунду (нормалізовані)")
    axes[2, 0].set_ylabel("Використання CPU")
    axes[2, 0].legend(loc='upper right')

    axes[2, 1].set_title("Похибки факторіальних многочленів (Логарифмічна шкала)", fontsize=10)
    axes[2, 1].set_xlabel("Запити за секунду (нормалізовані)")
    axes[2, 1].set_ylabel("Похибка (лог)")
    axes[2, 1].set_yscale('log')  # Вмикаємо логарифмічну шкалу
    axes[2, 1].set_ylim(1e-17, 1)
    axes[2, 1].legend(loc='lower center')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()