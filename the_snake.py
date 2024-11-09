from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс"""

    def __init__(self, position=None, body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта"""
        raise NotImplementedError

    def draw_section(self, position):
        """Метод отрисовки ячейки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self, occupied_positions=[((SCREEN_WIDTH // 2),
                                                      (SCREEN_HEIGHT // 2))]):
        """Метод для установки положения яблока"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        while self.position in occupied_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        #  В методе randomize_pozition я передал параметр occupied_positions,
        #  который по умолчанию равен центральной клетке поля,
        #  в которой появляется змея.
        #  Это сделано для того, чтобы яблоко при первой его генерации
        #  случайно не появилось в точке спавна змеи, то есть в клетке,
        #  уже занятой змеей.
        #  В остальных случаях occupied_pozitions будет
        #  содержать координаты змеи.
        #  Пока у меня больше нет мыслей как еще можно
        #  реализовать этод метод

    def draw(self):
        """Метод отрисовки яблока"""
        self.draw_section(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, обновляющий позицию змейки"""
        self.get_head_position()
        self.update_direction()

        old_head = self.positions[0]
        x, y = self.direction
        new_head = ((old_head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                    (old_head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки"""
        for position in self.positions:
            self.draw_section(position)

    def get_head_position(self):
        """Функция, возвращающая позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Функция сброса змейки в начальное состояние"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([RIGHT, UP, DOWN, LEFT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция"""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if len(snake.positions
               ) > 4 and snake.positions[0] in snake.positions[4:]:
            snake.reset()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            occupied_positions = snake.positions
            apple.randomize_position(occupied_positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
