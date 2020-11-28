from math import pi
from CourseResources import easy_shaders as es
from CourseResources import basic_shapes as bs
from CourseResources import scene_graph as sg
from CourseResources import transformations as tr
from OpenGL.GL import *


class Wall(object):

    def __init__(self, grid_size):

        # Basics variables set up
        self.total_grid = grid_size
        self.grid_unit = 2 / self.total_grid

