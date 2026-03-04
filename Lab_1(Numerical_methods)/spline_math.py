import numpy as np


def solve_tridiagonal(alpha: np.ndarray, beta: np.ndarray, gamma: np.ndarray, delta: np.ndarray) -> np.ndarray:
    """
    Розв'язує систему лінійних алгебраїчних рівнянь з трьохдіагональною матрицею методом прогонки.
    """
    n = len(delta)
    a = np.zeros(n)
    b = np.zeros(n)
    x = np.zeros(n)

    #  прогонка пряма
    a[1] = -gamma[1] / beta[1]
    b[1] = delta[1] / beta[1]

    for i in range(2, n - 1):
        denominator = alpha[i] * a[i - 1] + beta[i]
        a[i] = -gamma[i] / denominator
        b[i] = (delta[i] - alpha[i] * b[i - 1]) / denominator

    # зворотна прогонка
    x[n - 1] = 0.0  #  0, бо кривизна в кінці = 0 з умови вільного сплайна

    for i in range(n - 2, 0, -1):
        x[i] = a[i] * x[i + 1] + b[i]

    x[0] = 0.0  # Жорстко задаємо 0 для початку (умова вільного сплайна)

    return x


def calculate_spline_coefficients(x: np.ndarray, y: np.ndarray) -> tuple:
    """
    Обчислює коефіцієнти a, b, c, d для кубічного сплайна.
    """
    n = len(x)
    h = np.diff(x)

    alpha = np.zeros(n)
    beta = np.zeros(n)
    gamma = np.zeros(n)
    delta = np.zeros(n)

    # Формування системи рівнянь
    for i in range(1, n - 1):
        alpha[i] = h[i - 1]
        beta[i] = 2 * (h[i - 1] + h[i])
        gamma[i] = h[i]
        delta[i] = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

    # Знаходимо коефіцієнти c (метод прогонки)
    c = solve_tridiagonal(alpha, beta, gamma, delta)

    a_coef = np.zeros(n - 1)
    b_coef = np.zeros(n - 1)
    d_coef = np.zeros(n - 1)

    # Обчислення інших коефіцієнтів
    for i in range(n - 1):
        a_coef[i] = y[i]
        b_coef[i] = (y[i + 1] - y[i]) / h[i] - (h[i] / 3) * (c[i + 1] + 2 * c[i])
        d_coef[i] = (c[i + 1] - c[i]) / (3 * h[i])

    return a_coef, b_coef, c[:-1], d_coef


def evaluate_spline(x_eval: np.ndarray, x_nodes: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray,
                    d: np.ndarray) -> np.ndarray:
    """
    Обчислює значення функції сплайна для заданого масиву точок x_eval.
    """
    y_eval = []
    for xi in x_eval:
        for i in range(len(x_nodes) - 1):
            if x_nodes[i] <= xi <= x_nodes[i + 1] or i == len(x_nodes) - 2:
                dx = xi - x_nodes[i]
                yi = a[i] + b[i] * dx + c[i] * dx ** 2 + d[i] * dx ** 3
                y_eval.append(yi)
                break
    return np.array(y_eval)