import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid=self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid=self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

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
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid=[[0]*self.cell_width for i in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.choice([0,1])
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i,line in enumerate(self.grid):
            for j,cell in enumerate(line):
                color = pygame.Color('white')
                if cell: color=pygame.Color('green')
                pygame.draw.rect(self.screen, color, (j*self.cell_size, i*self.cell_size,self.cell_size,self.cell_size))

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
                    cells.append(self.grid[i][j])
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
        newgrid=self.create_grid(False)
        for i,line in enumerate(self.grid):
            for j,this in enumerate(line):
                cell=(i,j)
                neighbours_count=sum(self.get_neighbours(cell))
                if self.grid[i][j] == 1:
                    if neighbours_count in [2,3]:
                        newgrid[i][j]=1
                    else:
                        newgrid[i][j]=0
                else:
                    if neighbours_count==3:
                        newgrid[i][j]=1
                    else:
                        newgrid[i][j]=0
        return newgrid

if __name__ == "__main__":
    widht=int(input('width:\n'))
    height=int(input('height:\n'))
    cell_size=int(input('cell size:\n'))
    speed=int(input('speed:\n'))
    game=GameOfLife(widht,height,cell_size,speed)
    game.run()
