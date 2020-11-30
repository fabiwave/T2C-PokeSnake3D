from random import randint

import numpy as np
from OpenGL.GL import *

from CourseResources import easy_shaders as es
from CourseResources import scene_graph2 as sg
from CourseResources import transformations2 as tr
from CourseResources.obj_reader import readOBJ


class Apple(object):

    def __init__(self, grid_size):
        # Basics variables set up
        self.total_grid = grid_size
        self.grid_unit = self.grid_unit = 2 / self.total_grid

        # Object to model the apple
        gpu_carrot = es.toGPUShape(
            shape=readOBJ("/home/fabiwave/PycharmProjects/T2C-PokeSnake3D/T2/MVC/Models/Objects/carrot.obj",
                          (1, 1, 0)))
        carrot = sg.SceneGraphNode("carrot")

        # Translation delta for adjustment of the snake in the grid
        self.t_delta = 0
        if self.total_grid % 2 == 0:
            self.t_delta = self.grid_unit / 2

        # Generation of the random position in the grid
        half_grid = int((self.total_grid - 2) / 2)
        if self.total_grid % 2 == 0:
            half_grid = half_grid - 1

        random_x = randint(-half_grid, half_grid)
        random_y = randint(-half_grid, half_grid)
        x_adjusted = self.t_delta + (random_x * self.grid_unit)
        y_adjusted = self.t_delta + (random_y * self.grid_unit)

        # Transformations related to the object
        carrot.transform = tr.matmul([
            tr.uniformScale(self.grid_unit),
            tr.rotationX(np.pi / 4),
            tr.translate(x_adjusted, y_adjusted, 0)])
        carrot.childs += [gpu_carrot]

        # Designation of the previous apple as the model of this class
        self.model = carrot
        self.pos_x = x_adjusted
        self.pos_y = y_adjusted

    # Draws the apple node into the scene
    def draw(self, pipeline_light, projection, view):

        glUseProgram(pipeline_light.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_light.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_light.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(sg.findNode(self.model, 'carrot'), pipeline_light)

    # Returns the position of the apple
    def get_position(self):
        return [self.pos_x, self.pos_y]

    # Updates the position of the model
    def update_pos(self):
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)

    # Changes the position of the apple in the grid
    def respawn(self, snake):

        half_grid = int((self.total_grid - 2) / 2)
        if self.total_grid % 2 == 0:
            half_grid = half_grid - 1

        random_x = randint(-half_grid, half_grid)
        random_y = randint(-half_grid, half_grid)
        pos_x = self.t_delta + (random_x * self.grid_unit)
        pos_y = self.t_delta + (random_y * self.grid_unit)

        # If the position its in the snake, it has to be regenerated
        while snake.check_in_snake([pos_x, pos_y]):
            random_x = randint(-half_grid, half_grid)
            random_y = randint(-half_grid, half_grid)
            pos_x = self.t_delta + (random_x * self.grid_unit)
            pos_y = self.t_delta + (random_y * self.grid_unit)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.update_pos()
