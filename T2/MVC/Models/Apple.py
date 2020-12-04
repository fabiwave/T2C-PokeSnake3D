from math import pi
from random import randint

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
                          (1, 102 / 255, 178 / 255)))
        body = sg.SceneGraphNode("body")
        body.transform = tr.matmul([
            tr.uniformScale(self.grid_unit),
            tr.rotationX(pi / 2)])
        body.childs += [gpu_carrot]

        apple = sg.SceneGraphNode('carrot')
        apple.childs += [body]

        # Translation delta for adjustment of the snake in the grid
        self.t_delta = 0
        if self.total_grid % 2 == 0:
            self.t_delta = self.grid_unit / 2

        # Generation of the random position in the grid
        half_grid = int((self.total_grid - 2) / 2)
        if self.total_grid % 2 == 0:
            half_grid = half_grid - 1

        half_grid = int((self.total_grid - 2) / 2)
        if self.total_grid % 2 == 0:
            half_grid = half_grid - 1

        random_x = randint(-half_grid, half_grid)
        random_y = randint(-half_grid, half_grid)

        self.model = apple
        self.pos_x = self.t_delta + (random_x * self.grid_unit)
        self.pos_y = self.t_delta + (random_y * self.grid_unit)
        self.eaten = 0
        self.light_z = 10
        # Translation of the Apple to the random position
        self.model.transform = tr.translate(self.t_delta + (random_x * self.grid_unit),
                                            self.t_delta + (random_y * self.grid_unit), 0)

    # Draws the apple node into the scene
    def draw(self, pipeline_light, projection, view):

        # light settings
        self.light_setting(pipeline_light, view)
        # gl program to draw the carrot itself
        glUseProgram(pipeline_light.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_light.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_light.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(sg.findNode(self.model, 'carrot'), pipeline_light)

    def light_setting(self, pipeline_light, view):
        # Shininess of the object and z-location of the light depending on the amount of respawns
        shiny = 100
        z = 10
        if self.eaten % 4 == 0 and self.eaten != 0:
            shiny = 1
            z = 1

        camera_view = view[0]
        glUseProgram(pipeline_light.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "lightPosition"), 0, 0, z)
        glUniform3f(glGetUniformLocation(pipeline_light.shaderProgram, "viewPosition"), camera_view[0],
                    camera_view[1], camera_view[2], )
        glUniform1ui(glGetUniformLocation(pipeline_light.shaderProgram, "shininess"), shiny)
        glUniform1f(glGetUniformLocation(pipeline_light.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline_light.shaderProgram, "linearAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline_light.shaderProgram, "quadraticAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline_light.shaderProgram, "quadraticAttenuation"), 0.01)

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
        self.eaten += 1
