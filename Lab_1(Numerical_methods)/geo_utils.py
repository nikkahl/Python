import numpy as np

def calculate_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Обчислює відстань між двома точками на сфері за формулою Хаверсіна.

    Args:
        lat1 (float): Широта першої точки у градусах.
        lon1 (float): Довгота першої точки у градусах.
        lat2 (float): Широта другої точки у градусах.
        lon2 (float): Довгота другої точки у градусах.

    Returns:
        float: Відстань між точками у метрах.
    """
    r_earth = 6371000  # Радіус Землі в метрах
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1) # переведення широти довготи в радіанси
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2)**2
    return 2 * r_earth * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    #отримуємо дистанцію по дузі, відстаь між двома координатами.