import numpy as np
import matplotlib.pyplot as plt
import random

# Параметры системы
GRID_SIZE = 50  # Размер сетки (50x50)
PROB_GREEN = 0.45  # Вероятность появления зеленых агентов
PROB_YELLOW = 0.45  # Вероятность появления желтых агентов
PROB_EMPTY = 0.1  # Вероятность пустых клеток
ITERATIONS = 10  # Количество итераций симуляции


def create_environment(size, prob_green, prob_yellow, prob_empty):
    """Создает начальную сетку с заданными вероятностями для разных типов агентов (зеленые, желтые) и пустых клеток."""
    return np.random.choice(
        [0, 1, 2], size=(size, size), p=[prob_empty, prob_green, prob_yellow]
    )


def satisfies_preference(matrix, row, col):
    """Проверяет, удовлетворен ли агент, находящийся в клетке (row, col)."""
    if matrix[row, col] == 0:
        return True  # Пустая клетка всегда "счастлива"

    group = matrix[row, col]  # Группа (тип агента) на текущей клетке
    # Собираем список соседей, используя циклы для проверки клеток вокруг
    neighbors = [
        matrix[i % GRID_SIZE, j % GRID_SIZE]
        for i in range(row - 1, row + 2)
        for j in range(col - 1, col + 2)
        if (i != row or j != col) and (0 <= i < GRID_SIZE) and (0 <= j < GRID_SIZE)
    ]
    # Если среди соседей есть хотя бы 2 агента того же типа, агент считается удовлетворенным
    return neighbors.count(group) >= 2


def relocate_individuals(matrix):
    """Перемещает неудовлетворенных агентов в пустые ячейки."""
    # Находим все клетки с неудовлетворенными агентами (непустые клетки, у которых нет 2 соседей того же типа)
    dissatisfied = [
        (x, y)
        for x in range(GRID_SIZE)
        for y in range(GRID_SIZE)
        if matrix[x, y] != 0 and not satisfies_preference(matrix, x, y)
    ]
    # Находим все пустые клетки
    empty_slots = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if matrix[x, y] == 0]

    random.shuffle(dissatisfied)  # Случайное перемешивание неудовлетворенных агентов для разнообразия перемещений

    # Для каждого неудовлетворенного агента находим пустую клетку и перемещаем его туда
    for x, y in dissatisfied:
        if empty_slots:
            new_position = random.choice(empty_slots)  # Выбираем случайную пустую клетку
            empty_slots.remove(new_position)  # Убираем выбранную клетку из списка пустых
            matrix[new_position], matrix[x, y] = matrix[x, y], 0  # Перемещаем агента


def display_grid(matrix, iteration):
    """Отображает текущее состояние сетки на графике."""
    # Создаем пользовательскую цветовую карту: 0 - белый (пустая клетка), 1 - зеленый (зеленые агенты), 2 - оранжевый (желтые агенты)
    color_map = {
        0: (0, 0, 0),  # Черный (пустая клетка)
        1: (0, 0.39, 0),  # Темно-зеленый (зеленый агент)
        2: (1, 0.65, 0),  # Оранжевый (желтый агент)
    }

    # Преобразуем матрицу в изображение, где каждому значению в матрице соответствует свой цвет
    color_grid = np.zeros((matrix.shape[0], matrix.shape[1], 3))
    for x in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            color_grid[x, y] = color_map[matrix[x, y]]

    # Отображаем сетку для текущей итерации
    plt.figure()
    plt.imshow(color_grid, interpolation='nearest')
    plt.title(f'Итерация {iteration}')  # Заголовок с номером итерации
    plt.axis('off')  # Убираем оси


def run_simulation(steps):
    """Основной цикл симуляции, которая выполняется заданное количество итераций."""
    # Инициализируем начальную среду
    environment = create_environment(GRID_SIZE, PROB_GREEN, PROB_YELLOW, PROB_EMPTY)

    # Запускаем симуляцию на заданное количество шагов
    for step in range(steps):
        display_grid(environment, step)  # Отображаем текущее состояние сетки
        relocate_individuals(environment)  # Перемещаем неудовлетворенных агентов

    # Показываем все изображения после завершения симуляции
    plt.show()


if __name__ == "__main__":
    # Запускаем симуляцию на 10 итераций
    run_simulation(ITERATIONS)
