import logging
import sys 

logger = logging.getLogger(__name__)
ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"


def decrypt_text(ciphertext: str, base: int) -> str:      #анотація типу повернення 3.5
    """Decrypts text using a progressive Caesar cipher.

    Args:
        ciphertext: The encrypted string containing only allowed characters.
        base: The initial shift value for the first character.

    Returns:
        The fully decrypted string.
    """
    decrypted = ""   #49  

    for i, char in enumerate(ciphertext):      
        if char not in ALPHABET:
            continue 
    
  #  for i in range(len(ciphertext)):
   #     char = ciphertext[i]  
    #    if char not in ALPHABET:
      #      continue
    
        shift = base + i
        char_idx = ALPHABET.index(char)
        new_idx = (char_idx - shift) % len(ALPHABET)
        decrypted += ALPHABET[new_idx]
        
    return decrypted

#ковзне вікно:  перебираєм які літери в якій кількості в ключі -> порівнюємо з послідовністю тої самої довжини в розшифрованому тексті, порівнюємо збіг і кількість літер. 
def get_char_frequencies(text: str) -> dict[str, int]:
    """Calculates the frequency of each character in a string.

    Args:
        text: The string to analyze.

    Returns:
        A dictionary with characters as keys and their counts as values.
    """
    freq = {} #64 
    for char in text:
        freq[char] = freq.get(char, 0) + 1   #СИНТАКСИС: словник[ключ] = значення
    return freq


def find_anagram_indices(text: str, key: str) -> list[int]:
    """Finds starting indices of all anagrams of the key within the text.

    Args:
        text: The full string to search within.
        key: The substring anagram to look for.

    Returns:
        A list of starting indices where the anagram matches.
    """
    key_len = len(key)
    text_len = len(text)     #шоб не переходило за межі довжини слова
    indices = []

    if key_len > text_len or key_len == 0:
        return indices

    target_freq = get_char_frequencies(key)

    # Використовуємо ковзне вікно для пошуку збігів по частоті символів
    for i in range(text_len - key_len + 1):   #Off-by-one error range не включає задану межу тому +1
        window = text[i:i + key_len]        #0 до 0+5  рамки
        window_freq = get_char_frequencies(window)
        if window_freq == target_freq:
            indices.append(i)

    return indices


def crack_cipher(ciphertext: str, keys: list[str]) -> dict | None:
    """Attempts to crack the cipher by finding the correct base shift.

    Args:
        ciphertext: The encrypted string.
        keys: A list of key strings that must exist as anagrams in the text.

    Returns:
        A dictionary with 'base', 'decrypted_text', and 'key_indices' if successful,
        otherwise None.
    """
    for base in range(len(ALPHABET)):
        decrypted = decrypt_text(ciphertext, base)
        all_keys_found = True
        key_indices = {}

        for key in keys:
            indices = find_anagram_indices(decrypted, key)
            if not indices:
                all_keys_found = False
                break
            key_indices[key] = indices

        if all_keys_found:
            logger.info(f"Cipher successfully cracked! Found valid base: {base}")
            return {
                "base": base,
                "decrypted_text": decrypted,
                "key_indices": key_indices
            }

    logger.warning(f"Failed to crack cipher for text: {ciphertext}")
    return None