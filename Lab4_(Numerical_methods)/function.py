import math

def M(t):
    """Модель вологості ґрунту: M(t) = 50 * e^(-0.1*t) + 5 * sin(t)"""
    # t передається з main.py (зазвичай це наше t0 = 1.0)
    return 50 * math.exp(-0.1 * t) + 5 * math.sin(t)


def exact_derivative(t):
    """Точна аналітична похідна: M'(t) = -5 * e^(-0.1*t) + 5 * cos(t)"""
    # t = 1.0, повертає точну швидкість (наш еталон exact_val ≈ -1.789)
    return -5 * math.exp(-0.1 * t) + 5 * math.cos(t)


def forward_difference(func, x0, h):
    """Апроксимація (Права різниця)"""
    # func = M, x0 = 1.0, h = 1.0 (використовуємо великий крок суто для малювання 3-го графіка)
    return (func(x0 + h) - func(x0)) / h


def backward_difference(func, x0, h):
    """Апроксимація (Ліва різниця)."""
    # func = M, x0 = 1.0, h = 1.0 (також лише для 3-го графіка)
    return (func(x0) - func(x0 - h)) / h


def central_difference(func, x0, h):
    """Базова апроксимація (Центральна різниця)."""
    # func = M, x0 = 1.0, h = 0.001 (наш головний і найкращий робочий крок)
    return (func(x0 + h) - func(x0 - h)) / (2 * h)


def runge_romberg(d_h, d_2h):
    """Уточнення Рунге-Ромберга"""
    # d_h = швидкість при кроці 0.001
    # d_2h = швидкість при кроці 0.002
    # Похибка центральної різниці пропорційна h^2. Збільшуємо крок у 2 рази -> похибка росте в 4 рази.
    return d_h + (d_h - d_2h) / 3


def aitken_method(d_h, d_2h, d_4h):
    """Уточнення Ейткена"""
    # Передаємо ТРИ значення швидкості:
    # d_h (крок 0.001), d_2h (крок 0.002), d_4h (крок 0.004)
    # Алгоритм бачить, як ШВИДКО зростає похибка між цими трьома результатами, і знищує її

    # чисельник: середня швидкість^2 мінус (найгірша швидкість * найкраща швидкість)
    numerator = d_2h ** 2 - d_4h * d_h

    # знаменник: 2 * середня швидкість мінус (найгірша + найкраща)
    denominator = 2 * d_2h - (d_4h + d_h)

    if denominator == 0:
        return d_h  # Захист від ділення на нуль
    return numerator / denominator


def aitken_accuracy_order(d_h, d_2h, d_4h):
    """Оцінка порядку точності p за Ейткеном"""
    # Ті самі три швидкості (з кроками 0.001, 0.002, 0.004).
    # Повертає значення p_order (близько 2.0)
    numerator = abs(d_4h - d_2h)
    denominator = abs(d_2h - d_h)
    if denominator == 0 or numerator == 0:
        return None
    return (1 / math.log(2)) * math.log(numerator / denominator)