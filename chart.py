import multiprocessing as mul
import time
import matplotlib.pyplot as plt
import numpy as np
from hash import check_hash


def charting(card: str) -> None:
    """
    Функция для рисования графика
    """
    times = np.empty(shape=0)
    card = card[:6]
    items = [(i, card) for i in range(99999, 10000000)]
    for i in range(1, 8):
        start = time.time()
        with mul.Pool(i) as p:
            for i, result in enumerate(p.starmap(check_hash, items)):
                if result:
                    end = time.time() - start
                    times = np.append(times, end)
                    break
    plt.plot(range(len(times)), np.round(times, 2).tolist())
    plt.xlabel("Размер")
    plt.ylabel("Время в секундах")
    plt.show()
