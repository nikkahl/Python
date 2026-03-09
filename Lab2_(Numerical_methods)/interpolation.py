import numpy as np

def divided_differences(x_data, y_data):
    """Обчислення таблиці розділених різниць для многочлена Ньютона."""
    n = len(y_data)
    coef = np.zeros([n, n])
    coef[:, 0] = y_data  #всі рядки у 0 стовпці заповнюмо у
    for j in range(1, n): # рахунок ПО СТОВПЦЯХ з 1, бо стовпець вже заповнений
        for i in range(n - j):   #
            coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (x_data[i + j] - x_data[i])
    return coef[0, :] #для формули ньютона перший нульовий рядок всі значення стовпців.
# ділить на різницю diff

def newton_polynomial(x_data, coefs, x):
    """Обчислення значення многочлена Ньютона в точці x."""
    n = len(coefs)
    result = coefs[0]
    for i in range(1, n):
        term = coefs[i]
        for j in range(i):
            term *= (x - x_data[j])
        result += term
    return result

def forward_differences(y_data):
    """Обчислення скінченних різниць вперед для факторіального многочлена."""
    n = len(y_data)
    diffs = np.zeros([n, n])
    diffs[:, 0] = y_data
    for j in range(1, n):
        for i in range(n - j):
            diffs[i][j] = diffs[i + 1][j - 1] - diffs[i][j - 1]
    return diffs[0, :]
# віднімає різницю diff

def factorial_polynomial(diffs, t):
    """Обчислення значення факторіального многочлена за індексом t."""
    result = diffs[0]
    t_prod = 1
    factorial = 1
    for i in range(1, len(diffs)):
        t_prod *= (t - i + 1)
        factorial *= i
        result += (diffs[i] * t_prod) / factorial
    return result

def test_function(x):
    """
    Використовуємо синусоїду, щоб ідеально відтворити графіки з прикладу звіту.
    """
    return np.sin(2 * np.pi * x)