import re
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar, QPushButton)
from hash import SETTING, check_algorithm_luna, check_hash
import multiprocessing as mp
import sys
import time
from chart import charting


class Window(QMainWindow):
    def __init__(self) -> None:
        """
        Функция инициализации
        """
        super(Window, self).__init__()
        self.result_card = None
        self.size = None
        self.setWindowTitle('Поиск банковской карты')
        self.setFixedSize(600, 400)
        self.info = QLabel(self)
        self.info.setText("Выберите начало карты")
        self.info.setGeometry(225, 0, 500, 50)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setGeometry(100, 230, 400, 50)
        self.progress.hide()
        self.button_card = QPushButton('Найти карту', self)
        self.button_card.setGeometry(200, 100, 200, 50)
        self.button_card.clicked.connect(self.preparation)
        self.button_card.hide()
        self.result = QLabel(self)
        self.result.setGeometry(200, 150, 400, 100)
        self.pool_size = QtWidgets.QComboBox(self)
        self.pool_size.addItems([str(i) for i in range(1, 33)])
        self.pool_size.setGeometry(200, 50, 200, 50)
        self.pool_size.hide()
        self.number = QtWidgets.QComboBox(self)
        self.number.addItems(SETTING["begin_digits"])
        self.number.setGeometry(200, 20, 200, 50)
        self.number.activated[str].connect(self.on_activated)
        self.graph = QPushButton('Построить график', self)
        self.graph.setGeometry(200, 270, 200, 50)
        self.graph.clicked.connect(self.show_graph)
        self.graph.hide()
        self.show()

    def on_activated(self, text: str) -> None:
        """
        Функция присвоения номера
        """
        self.graph.hide()
        self.pool_size.show()
        try:
            self.number = int(re.findall('(\d+)', text)[0])
        except:
            self.number = SETTING['begin_digits'][0]
        self.pool_size.activated[str].connect(self.choose_pool)

    def choose_pool(self, text: str) -> None:
        """
        Функция присвоения размера пула
        """
        try:
            self.size = int(re.findall('(\d+)', text)[0])
        except:
            self.size = 0
        self.button_card.show()

    def preparation(self):
        """
        Функция подготовки линии прогресса и списка пула
        """
        items = [(i, self.number) for i in range(99999, 10000000)]
        start = time.time()
        self.progress.show()
        QApplication.processEvents()
        self.progress_bar(start, items)

    def progress_bar(self, start: float, items: list):
        """
        Функция отображает прогресс при поиске
        """
        with mp.Pool(self.size) as p:
            for i, result in enumerate(p.starmap(check_hash, items)):
                if result:
                    self.success(start, result)
                    p.terminate()
                    break
                self.update_progress_bar(i)
            else:
                self.result.setText('Не найдено')
                self.progress.setValue(0)

    def update_progress_bar(self, i: int):
        """
        Функция обновления прогресса
        """
        self.progress.setValue(int(i/9900000*100))
        QApplication.processEvents()

    def success(self, start: float, result: int):
        """
        Функция вывода информации о карте
        """
        self.result_card = result
        self.progress.setValue(100)
        end = time.time() - start
        result_text = f'Расшифрованный номер: {result}\n'
        result_text += f'Проверка алгоритма Луна: {check_algorithm_luna(result)}\n'
        result_text += f'Время: {end:.2f} секунд'
        self.result.setText(result_text)
        self.graph.show()

    def show_graph(self):
        charting(self.result_card)


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
