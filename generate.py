from dataclasses import dataclass, field
import numpy as np
from random import random, randint

@dataclass
class MazeCell:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=list)


def find(x):
    global cells
    return cells[x[0]][x[1]].component

def union(x, y):
    global roots
    global cells
    bool_arr = (roots == cells[x[0]][x[1]].component)
    f = np.count_nonzero(bool_arr)
    bool_arr = (roots == cells[y[0]][y[1]].component)
    s = np.count_nonzero(bool_arr)
    if f >= s:
        new_root = cells[x[0]][x[1]].component
        old_root = cells[y[0]][y[1]].component
    else:
        old_root = cells[x[0]][x[1]].component
        new_root = cells[y[0]][y[1]].component
    for i in range(len(roots)):
        if roots[i] == old_root:
            roots[i] = new_root

    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if cells[i][j].component == old_root:
                cells[i][j].component = new_root

def generate_maze(N) -> list[list[MazeCell]]:
    global cells
    cells = []
    global roots
    roots = []
    for i in range(N):
        cells.append([])
        for j in range(N):
            cells[i].append(MazeCell(i, j, i * N + j, False, [True, True, True, True]))
            roots.append(i * N + j)
    roots = np.array(roots)

    while len(np.unique(roots)) > 1:
        x = randint(0, N - 1)
        y = randint(0, N - 1)
        neigbors = []
        if x != 0:
            neigbors.append((x - 1, y))
        if x != N -1:
            neigbors.append((x + 1, y))
        if y != 0:
            neigbors.append((x, y - 1))
        if y != N - 1:
            neigbors.append((x, y + 1))
        r_neigbour = neigbors[randint(0, len(neigbors) - 1)]
        if find((x, y)) != find(r_neigbour):
            if x < r_neigbour[0]:
                cells[x][y].walls[2] = False
                cells[r_neigbour[0]][r_neigbour[1]].walls[0] = False
            elif x > r_neigbour[0]:
                cells[x][y].walls[0] = False
                cells[r_neigbour[0]][r_neigbour[1]].walls[2] = False

            elif y < r_neigbour[1]:
                cells[x][y].walls[1] = False
                cells[r_neigbour[0]][r_neigbour[1]].walls[3] = False
            elif y > r_neigbour[1]:
                cells[x][y].walls[3] = False
                cells[r_neigbour[0]][r_neigbour[1]].walls[1] = False
            union((x, y), r_neigbour)
    cells[0][0].is_open = True
    cells[0][0].walls[0] = False
    cells[N - 1][N - 1].is_open = True
    cells[N - 1][N - 1].walls[2] = False
    return cells
