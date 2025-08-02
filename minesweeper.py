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
    closed = '🔒 '
    mine = '💣'

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

    def show_top_bar(self):
        """Метод отображения верхнего ряда цифр."""
        left_margin = 5
        one_column_size = 4
        top_numbers = [i + 1 for i in range(self._size)]
        for num in top_numbers:
            if num == 1:
                print(f'{' ' * left_margin}{num}   ', end='')
            elif num < 10:
                print(f'{num}   ', end='')
            else:
                print(f'{num}  ', end='')
        print()
        print(f'{' ' * (left_margin - 1)}{'_' * self._size * one_column_size}')

    def show(self):
        """Метод отображения текущего состояния игрового поля."""
        self.show_top_bar()
        for i, row in enumerate(self.field):
            print(
                  f' {i + 1} |' if i < 9 else f'{i + 1} |',
                  *map(
                      lambda x: f'{self.closed}' if not x.is_open
                      else f'{self.mine}' if x.is_mine else
                      f' {x.mines_arond} ', row
                    )
                )

    def show_all(self):
        """Метод показа всех ячеек в открытом состоянии."""
        self.show_top_bar()
        for i, row in enumerate(self.field):
            print(
                  f' {i + 1} |' if i < 9 else f'{i + 1} |',
                  *map(
                      lambda x: f'{self.mine} ' if x.is_mine else
                      f' {x.mines_arond} ', row
                    )
                )

    def make_turns(self):
        """Метод совершения ходов игроком."""
        while True:
            try:
                x = int(input('Please enter the row number: ')) - 1
                y = int(input('Please enter the column number: ')) - 1
                if self.field[x][y].is_open:
                    print('This cell is already open. Choose another one.\n')
                    continue
            except ValueError or IndexError:
                print(f'Row and column numbers must be 1 to {self._size}.\n')
                continue
            print()
            self.field[x][y].is_open = True
            if self.field[x][y].is_mine:
                self.show_all()
                print("It's a mine! The game is over!")
                break
            self.show()


def main():
    size = 10
    mines = 12
    field = MineField(size, mines)
    field.show()
    field.make_turns()
    input('Press ENTER to exit.')


if __name__ == '__main__':
    main()
