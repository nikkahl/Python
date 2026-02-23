import logging
from cipher_logic import crack_cipher

# pep 282 стандарт берем
logging.basicConfig(
    level=logging.INFO,
    format = "%(levelname)s, %(message)s" #створює іменований логер (щоб уникнути змішування логів)
)

logger = logging.getLogger(__name__)


def run_test_cases():
    """Runs predefined test cases for the cipher decoding algorithm."""
    
    test_cases = [
        {
            "description": "PDF Example 1",
            "ciphertext": "kos0kw62rzz",
            "keys": ["opyhtn"]
        },
        {
            "description": "Custom Short Test",
            "ciphertext": "jgnnq", # 'hello' with base 2
            "keys": ["loh"]
        },
        {
            "description": "Multiple Keys Test",
            "ciphertext": "3tiuzyrg4eaz7704ahge", # 'welcome2python3intro' with base 7
            "keys": ["3poyrth", "2emlweoc"] #cписок 1+ keys
        }
    ]

    for case in test_cases:   # можна було використовувати enumerate для індексуванння (логи)
        #можна сюди присвоїти змінній result славник, а тоді через іф перевірити чи словник не пустий ----> а можна моржа шоб одразу присвоїти 

        if result := crack_cipher(case["ciphertext"], case["keys"]):     #If result:       
            logger.info(f"Resulting Base: {result['base']}")
            logger.info(f"Decrypted Text: {result['decrypted_text']}")
            logger.info(f"Key Indices: {result['key_indices']}")
        else:
            logger.error("Could not find a valid base for this test case.")
        
        logger.info("-" * 40)


if __name__ == "__main__":
    run_test_cases()