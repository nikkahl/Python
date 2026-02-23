import json
import random

def generate_contacts(file_path="contacts.json", count=10000):
    first_names = ["Андрій", "Олена", "Іван", "Марія", "НенавиджуМатематику", "Дмитро", "Анна", "Сергій", "Ольга", "Ніка", "Пайтон"]
    last_names = ["Шевченко", "Коваленко", "Бондар", "Ткач", "Лисенко", "Кравченко", "Moore", "Moon", "Morse", "Фу", "ДА", "Галт"]
    
    contacts = []

    for i in range(count):
        full_name = f"{random.choice(last_names)} {random.choice(first_names)}"
        phone = f"0{random.randint(50, 99)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        
        contacts.append({"name": full_name, "phone": phone})

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    
    print(f"Файл '{file_path}' успішно створено!")

generate_contacts()