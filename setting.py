import json

SETTING = {
    'hash': 'e5c92fb926ffc9976ad06b46cc7eb656158f07b6e41a1666e005c9cd',
    'begin_digits': ["423078", '427401', '427414', '427415', '427421', '427423', '427424', '427429', '427434', '427435',
                     '427437', '427443', '427447', '427448', '427457', '427458', '427464', '427465', '427471', '427473',
                     '442198', '475794', '479583', '479586', '481778', '481781', '481782', '485463', '489798', '427601',
                     '427901', '466765', '467455'],
    'last_digits': '1217',
    'card_number': 'card_number.txt',
    'png_statistics': 'statistics.png'
}


def get_settings() -> None:
    """
    Функция открывает файл setting.json для записи в него SETTING
    """
    with open('setting.json', 'w') as fp:
        json.dump(SETTING, fp)


if __name__ == '__main__':
    get_settings()
