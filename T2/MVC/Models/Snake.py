from MVC.Models.SnakeSegment import SnakeSegment


class Snake(object):

    def __init__(self, grid_size, apple):
        # Basics variables set up
        self.head = SnakeSegment(grid_size)
        self.apple = apple
        self.alive = True
        self.grid_unit = 2 / grid_size

    # Draws the snake node into the scene
    def draw(self, pipeline_texture, projection, view):
        self.head.draw(pipeline_texture, projection, view)

    # Returns the position of the Snake
    def get_position(self):
        return self.head.get_position()

    # Moves the model to the left in the grid
    def move_left(self):
        self.head.move_left()

    # Moves the model to the right in the grid
    def move_right(self):
        self.head.move_right()

    # Moves the model down in the grid
    def move_down(self):
        self.head.move_down()

    # Moves the model up in the grid
    def move_up(self):
        self.head.move_up()

    # Sets the last movement of the snake
    def set_last_move(self, orientation):
        self.head.set_last_move(orientation)

    # Continues the last movement of the snake
    def continue_move(self):
        self.head.continue_move()

    # Returns if the snake is colliding into a wall
    def wall_collision(self):
        return self.head.wall_collision()

    # Returns if the snake is colliding with a snake segment
    def snake_collision(self):
        return self.head.snake_collision()

    # Handles the apple been eaten by snake
    def eat_apple(self):
        current_pos = self.head.get_position()
        x_delta = abs(current_pos[0] - self.apple.get_position()[0])
        y_delta = abs(current_pos[1] - self.apple.get_position()[1])
        if x_delta <= (self.grid_unit / 4) and y_delta <= (self.grid_unit / 4):
            self.head.add_segment()
            self.apple.respawn(self)

    # Checks in all of the segments of the snake
    def check_in_snake(self, position):
        return self.head.check_in_snake(position)

    # Returns the last head mov
    def get_head_last_mov(self):
        return self.head.last_mov
