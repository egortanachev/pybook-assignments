import pathlib
import random

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cols` х `rows`.
        """
        grid=[[0]*self.cols for i in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.choice([0,1])
        return grid


    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        cells = []
        cell_neighbours = [[-1, -1], [1, 1], [0, 1], [1, 0], [-1, 1], [1, -1], [-1, 0], [0, -1]]
        for c in cell_neighbours:
            c[0] += cell[0]
            c[1] += cell[1]
        for c in cell_neighbours:
            i, j = c
            try:
                if i >= 0 and j >= 0:
                    cells.append(self.curr_generation[i][j])
            except IndexError:
                pass
        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
    def get_next_generation(self) -> Grid:
        new_greed = self.create_grid(False)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j]:
                    if sum(self.get_neighbours((i, j))) in [2, 3]:
                        new_greed[i][j] = 1
                elif sum(self.get_neighbours((i, j))) == 3:
                    new_greed[i][j] = 1
        return new_greed

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation=self.curr_generation
        self.curr_generation=self.get_next_generation()
        self.n_generation+=1


    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        is_exceeded=True
        if self.n_generation>self.max_generations:
            is_exceeded=False
        return is_exceeded

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        is_changing=False
        for i in range(self.rows):
            if self.prev_generation[i]!=self.curr_generation[i]:
                is_changing=True
        return is_changing

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid=[]
        file=open(filename,'r')
        for i,line in enumerate(file):
            grid.append([])
            for c in line[:-1]:
                grid[i].append(int(c))
        game_from_file=GameOfLife(size=(len(grid),len(grid[0])), randomize=False)
        game_from_file.curr_generation=grid
        return game_from_file

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file=open(filename,'w')
        for i in self.curr_generation:
            for c in i:
                file.write(str(c))
            file.write('\n')
