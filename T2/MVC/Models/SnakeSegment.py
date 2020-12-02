from math import pi

from OpenGL.GL import *

from CourseResources import basic_shapes as bs
from CourseResources import easy_shaders as es
from CourseResources import scene_graph2 as sg
from CourseResources import transformations2 as tr


class SnakeSegment(object):

    def __init__(self, grid_size):
        # Basics variables set up
        self.total_grid = grid_size
        self.grid_unit = 2 / self.total_grid
        self.alive = True
        self.last_mov = "Up"
        self.theta = pi / 2
        self.next_segment = None
        self._rotations = {"Up": pi / 2, "Left": pi, "Down": 3 * pi / 2, "Right": 2 * pi}

        gpu_face = es.toGPUShape(
            bs.createTextureCube("/home/fabiwave/PycharmProjects/T2C-PokeSnake3D/T2/MVC/Models/Images/face.png"),
            GL_REPEAT, GL_NEAREST)
        gpu_skin = es.toGPUShape(
            bs.createTextureCube("/home/fabiwave/PycharmProjects/T2C-PokeSnake3D/T2/MVC/Models/Images/body.png"),
            GL_REPEAT, GL_NEAREST)

        # Creation of body node in the graph
        head = sg.SceneGraphNode("head")
        head.transform = tr.matmul([tr.scale(1, 1, 1), tr.translate(0, 0, 0)])
        head.childs += [gpu_skin]

        face = sg.SceneGraphNode('face')
        face.transform = tr.matmul([tr.scale(0.95, 0.95, 0.95), tr.translate(0.1, 0, 0)])
        face.childs += [gpu_face]

        snake = sg.SceneGraphNode('bodyTR')
        snake.transform = tr.scale(self.grid_unit, self.grid_unit, self.grid_unit)
        snake.childs += [head, face]

        # Addition the snake to the scene graph node
        transform_snake = sg.SceneGraphNode('snakeTR')
        transform_snake.childs += [snake]

        # Translation delta for adjustment of the snake in the grid
        self.t_delta = 0
        if self.total_grid % 2 == 0:
            self.t_delta = self.grid_unit / 2

        # Designation of the previous snake as the model of this class
        self.model = transform_snake
        self.pos_x = self.t_delta
        self.pos_y = self.t_delta

        # Translation of the snake to the center position
        self.model.transform = tr.matmul([tr.translate(self.t_delta, self.t_delta, 0), tr.rotationZ(pi / 2)])

    def draw(self, pipeline_texture, projection, view):
        # To draw the texture parts of the snake
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(sg.findNode(self.model, 'snakeTR'), pipeline_texture)
        if self.next_segment is not None:
            self.next_segment.draw(pipeline_texture, projection, view)

    # Returns the position of the Snake
    def get_position(self):
        return [self.pos_x, self.pos_y]

    # Sets the position of the snake
    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    # Updates the position of the model
    def update_pos(self, new_dir="Up"):
        rotation = self.rotate(new_dir)
        translation = tr.translate(self.pos_x, self.pos_y, 0)
        self.model.transform = tr.matmul([translation, rotation])
        if self.next_segment is not None:
            self.next_segment.continue_move()
            self.next_segment.set_last_move(self.last_mov)

    # Moves the model to the left in the grid
    def move_left(self):
        if self.alive:
            self.pos_x -= self.grid_unit
            self.update_pos("Left")
            self.last_mov = "Left"

    # Moves the model to the right in the grid
    def move_right(self):
        if self.alive:
            self.pos_x += self.grid_unit
            self.update_pos("Right")
            self.last_mov = "Right"

    # Moves the model down in the y component in the grid
    def move_down(self):
        if self.alive:
            self.pos_y -= self.grid_unit
            self.update_pos("Down")
            self.last_mov = "Down"

    # Moves the model up in the y component in the grid
    def move_up(self):
        if self.alive:
            self.pos_y += self.grid_unit
            self.update_pos("Up")
            self.last_mov = "Up"

    # Returns the last movement of the snake
    def get_last_move(self):
        return self.last_mov

    # Sets the last movement of the snake
    def set_last_move(self, orientation):
        self.last_mov = orientation

    # Continues the last movement of the snake
    def continue_move(self):
        if not self.wall_collision():
            if self.last_mov == "Right":
                self.move_right()
            elif self.last_mov == "Left":
                self.move_left()
            elif self.last_mov == "Down":
                self.move_down()
            elif self.last_mov == "Up":
                self.move_up()

    # Returns if the snake is colliding into a wall
    def wall_collision(self):
        wall_boolean = False
        wall_pos = 1 - self.grid_unit

        if self.pos_x >= wall_pos or self.pos_x <= -wall_pos or self.pos_y >= wall_pos or self.pos_y <= -wall_pos:
            self.alive = False
            wall_boolean = True

        return wall_boolean

    # Returns if the snake is colliding into itself
    def snake_collision(self):
        collision = False
        if self.next_segment is not None:
            if self.next_segment.check_in_snake([self.pos_x, self.pos_y]):
                collision = True
                self.alive = False
        return collision

    # Adds a segment to the snake
    def add_segment(self):
        if self.next_segment is not None:
            self.next_segment.add_segment()
        else:
            self.next_segment = SnakeSegment(self.total_grid)
            self.next_segment.move_to_last(self.get_position(), self.last_mov)

    # Checks in all of the segments of the snake
    def check_in_snake(self, position):
        current_pos = [self.pos_x, self.pos_y]
        x_delta = abs(current_pos[0] - position[0])
        y_delta = abs(current_pos[1] - position[1])
        if x_delta <= (self.grid_unit / 4) and y_delta <= (self.grid_unit / 4):
            return True
        elif self.next_segment is None:
            return False
        else:
            return self.next_segment.check_in_snake(position)

    # Returns the rotation
    def rotate(self, new_dir):
        rotation = self._rotations[new_dir]
        transform = tr.rotationZ(rotation)
        return transform

    def move_to_last(self, pos, previous_dir):
        if previous_dir == "Right":
            self.set_position(pos[0] - self.grid_unit, pos[1])
        elif previous_dir == "Left":
            self.set_position(pos[0] + self.grid_unit, pos[1])
        elif previous_dir == "Down":
            self.set_position(pos[0], pos[1] + self.grid_unit)
        elif previous_dir == "Up":
            self.set_position(pos[0], pos[1] - self.grid_unit)
        self.last_mov = previous_dir
        rotation = self.rotate(self.last_mov)
        translation = tr.translate(self.pos_x, self.pos_y, 0)
        self.model.transform = tr.matmul([translation, rotation])
