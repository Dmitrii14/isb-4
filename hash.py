import hashlib
import logging
from setting import SETTING

logger = logging.getLogger()
logger.setLevel('INFO')


def check_hash(card_center: int, card_begin: int) -> int:
    """
    Функция проверки совпадения хэша
    card_center - цифры середины номера карты
    card_begin - цифры начала номера карты
    """
    logging.info("Проверка хеша")
    card_number = str(card_begin) + str(card_center) + SETTING['last_digits']
    card_hash = hashlib.sha224(card_number.encode()).hexdigest()
    if SETTING['hash'] == card_hash:
        return card_number
    return False


def check_algorithm_luna(number: str) -> bool:
    """
    Функция проверки номера карты с использыванием алгоритма Луна
    number - номер карты
    """
    all_number = list(map(int, number))
    all_number = all_number[::-1]
    for i, num in enumerate(all_number):
        if i % 2 == 0:
            tmp = num*2
            if tmp > 9:
                tmp -= 9
            all_number[i] = tmp
    total_sum = sum(all_number)
    rem = total_sum % 10
    check_sum = (10 - rem if rem != 0 else 0)
    return True if check_sum == 7 else False
