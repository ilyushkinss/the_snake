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

    def __init__(self) -> None:
        self.position = None
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Метод отрисовки объекта"""
        raise NotImplementedError


class Apple(GameObject):
    """Класс, описывающий яблоко"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def randomize_position(self, snake_positions):
        """Метод для установки положения яблока"""
        while self.position in snake_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        """Метод, обновляющий позицию змейки"""
        self.get_head_position()
        if self.next_direction:
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
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        # head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        # pg.draw.rect(screen, self.body_color, head_rect)
        # pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

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
        if len(snake.positions) > 4 and snake.positions[0] in snake.positions[2:]:
            snake.reset()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake_positions = snake.positions
            apple.randomize_position(snake_positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
