from random import randint


class Cell:
    """Класс ячейки игрового поля."""

    def __init__(self, mines_arond=0, is_mine=False):
        # Количество мин вокруг ячейки.
        self.mines_arond = mines_arond
        # Является ли ячейка миной.
        self.is_mine = is_mine
        # Открыта ли ячейка.
        self.is_open = False


class MineField:
    """Класс игрового поля."""

    def __init__(self, size, mines):
        self._size = size
        self._mines = mines
        self.field = [
            [Cell() for _ in range(self._size)] for _ in range(self._size)
        ]
        self.initialize()

    def initialize(self):
        """Метод инициализации игрового поля."""
        # Вводим счетчик количества мин, которые нужно распределить.
        mines_left = self._mines
        # Распределяем мины по игровому полю в цикле.
        while mines_left > 0:
            x = randint(0, self._size - 1)
            y = randint(0, self._size - 1)
            # Если в выбранной рандомной ячейке уже есть мина, то
            # генерируем ряд и колонку заново.
            if self.field[x][y].is_mine:
                continue
            # Если предыдущая проверка не прошла, то в выбранной ячейке
            # меняем флаг is_mine на True.
            self.field[x][y].is_mine = True
            # Уменьшаем счетчик нераспределенных мин на 1.
            mines_left -= 1

        # Кортеж из относительных индексов вокруг ячейки.
        indx = (
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
            (1, 1)
        )
        # Для каждой ячейки, которая не является миной, считаем количество
        # мин вокруг нее.
        for x in range(self._size):
            for y in range(self._size):
                if not self.field[x][y].is_mine:
                    mine_count = sum(
                        (
                            self.field[x+i][y+j].is_mine for i, j in indx
                            if 0 <= x + i < self._size and (
                                    0 <= y + j < self._size
                                    )
                        )
                    )
                    # Записываем количество мин в атрибут mines_arond.
                    self.field[x][y].mines_arond = mine_count

    def show(self):
        """Метод отображения текущего состояния игрового поля."""
        for row in self.field:
            print(*map(lambda x: '#' if not x.is_open else '*' if x.mine else
                       x.mines_arond, row))
