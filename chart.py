import multiprocessing as mul
import time
import matplotlib.pyplot as plt
import numpy as np
from hash import check_hash


def charting(card: str) -> None:
    """
    Функция для рисования графика
    :type card: номер карты
    """
    times = np.empty(shape=0)
    card = card[:6]
    items = [(i, card) for i in range(1000000)]
    for i in range(4):
        start = time.time()
        with mul.Pool(i) as p:
            for i, result in enumerate(p.starmap(check_hash, items)):
                if result:
                    end = time.time() - start
                    times = np.append(times, end)
                    break
    plt.plot(range(len(times)), np.round(times, 2).tolist())
    plt.xlabel('Processes')
    plt.ylabel('Time')
    plt.title('Statistics')
    plt.bar(color='yellow', width=0.5)
    plt.show()
