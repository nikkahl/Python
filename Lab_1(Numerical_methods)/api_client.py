import requests

def fetch_elevation_data(url: str) -> list[dict]:
    """
    Виконує запит до Open-Elevation API та повертає список точок.

    Args:
        url (str): URL-адреса для запиту до API з координатами.

    Returns:
        list[dict]: Список словників з ключами 'latitude', 'longitude', 'elevation'.
    """
    response = requests.get(url)  #сервер open-elevation.com
    response.raise_for_status()
    data = response.json()   #текст на формат json для python
    return data["results"]