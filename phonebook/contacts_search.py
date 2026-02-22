import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

class PhoneBook:
    """A simple phone book implementation.

    Attributes:
        contact_list (list): A list of dictionaries containing contact data.
    """

    def __init__(self):
        """Initializes an empty contact list."""
        self.contact_list = []

    def load_data(self, json_file_path):
        """Loads data from a JSON file and sorts it by name.

        Args:
            json_file_path (str): The path to the JSON file containing contacts.
        """
        try:
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                self.contact_list = json.load(json_file)
            
            # Для бінарного пошуку список ОБОВ'ЯЗКОВО має бути відсортований
            self.contact_list.sort(key=lambda contact_record: contact_record["name"])
            logger.info(f"Завантажено {len(self.contact_list)} контактів.")
        except Exception as error_message:
            logger.error(f"Помилка завантаження файлу: {error_message}")

    def find_contacts(self, search_query):
        """Finds all contacts starting with the given query using binary search.

        Args:
            search_query (str): The name or surname to search for.

        Returns:
            list: A list of dictionaries containing the matched contacts.
        """
        lower_bound = 0
        upper_bound = len(self.contact_list) - 1
        first_match_index = -1

        # Бінарний пошук: ділимо список навпіл, поки не знайдемо збіг
        while lower_bound <= upper_bound:
            middle_index = (lower_bound + upper_bound) // 2
            current_contact_name = self.contact_list[middle_index]["name"]

            if current_contact_name.startswith(search_query):
                first_match_index = middle_index
                # Знайшли збіг, але продовжуємо шукати лівіше, 
                # щоб знайти НАЙПЕРШУ людину з таким прізвищем серед дублікатів
                upper_bound = middle_index - 1
            elif current_contact_name < search_query:
                lower_bound = middle_index + 1
            else:
                upper_bound = middle_index - 1

        if first_match_index == -1:
            return []

        matching_contacts = []
        # Оскільки список відсортований, всі однофамільці стоять поруч.
        # Просто йдемо від першого знайденого вправо, поки прізвище збігається.
        for current_index in range(first_match_index, len(self.contact_list)):
            current_record = self.contact_list[current_index]
            
            if current_record["name"].startswith(search_query):
                matching_contacts.append(current_record)
            else:
                break # Інші прізвища пішли, зупиняємо цикл
                
        return matching_contacts

my_phone_book = PhoneBook()
my_phone_book.load_data("contacts.json")

while True:
    user_search_query = input("\nВведіть прізвище для пошуку (або Enter для виходу): ").strip()

    match user_search_query:
        case "":
            break
        case searched_name:
            found_contacts = my_phone_book.find_contacts(searched_name)
            match found_contacts:
                case []:
                    logger.info(f"Запис '{searched_name}' не знайдено.")
                case matched_items:
                    logger.info(f"Знайдено записів: {len(matched_items)}")
                    for contact_record in matched_items:
                        logger.info(f"{contact_record['name']}: {contact_record['phone']}")