"""Классическая змейка на Pygame."""

from random import choice

import pygame

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый игровой объект с позицией и цветом."""

    def __init__(self, body_color=None):
        """Поместить объект в центр игрового поля."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовать объект в соответствии с его типом."""
        pass

    def draw_cell(self, position):
        """Нарисовать закрашенную клетку с рамкой."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое появляется в свободной клетке поля."""

    def __init__(self, occupied_positions=()):
        """Создать яблоко на случайной свободной клетке."""
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """Выбрать случайную свободную клетку или убрать яблоко."""
        occupied = set(occupied_positions)
        free_positions = [
            (column * GRID_SIZE, row * GRID_SIZE)
            for column in range(GRID_WIDTH)
            for row in range(GRID_HEIGHT)
            if (column * GRID_SIZE, row * GRID_SIZE) not in occupied
        ]
        self.position = choice(free_positions) if free_positions else None

    def draw(self):
        """Нарисовать яблоко, если для него есть свободная клетка."""
        if self.position is not None:
            self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка, тело которой хранится списком от головы до хвоста."""

    def __init__(self):
        """Создать змейку длиной в одну клетку."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Применить направление, выбранное игроком."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвинуть змейку на одну клетку и запомнить старый хвост."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def grow(self):
        """Вернуть убранную клетку хвоста после съедания яблока."""
        self.positions.append(self.last)
        self.length += 1
        self.last = None

    def draw(self):
        """Стереть след хвоста и нарисовать все сегменты змейки."""
        if self.last is not None:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Вернуть змейку в центр поля и направить вправо."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать стрелки и закрытие окна игры."""
    directions = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }
    direction_x, direction_y = game_object.direction
    opposite_direction = (-direction_x, -direction_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            direction = directions.get(event.key)
            if direction is not None and direction != opposite_direction:
                game_object.next_direction = direction


def main():
    """Запустить игру и обновлять поле до закрытия окна."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()
        if head == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
