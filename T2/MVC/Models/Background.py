import os

from OpenGL.GL import *

from CourseResources import basic_shapes as bs
from CourseResources import easy_shaders as es
from CourseResources import scene_graph2 as sg
from CourseResources import transformations2 as tr


class Background(object):

    def __init__(self, grid_size):
        # Basics variables set up
        self.total_grid = grid_size
        self.grid_unit = 2 / self.total_grid

        # Direction for relatives paths
        directory_path = os.path.abspath(os.path.dirname(__file__))
        image_path = os.path.join(directory_path, 'Images/grass.png')

        gpu_ground = es.toGPUShape(bs.createTextureCube(image_path), GL_REPEAT, GL_NEAREST)

        grass = sg.SceneGraphNode('grass')
        grass.transform = tr.matmul([tr.scale(2, 2, self.grid_unit), tr.translate(0, 0, -1)])
        grass.childs += [gpu_ground]

        ground = sg.SceneGraphNode('ground')
        ground.childs += [grass]

        self.model = ground

    def draw(self, pipeline_texture, projection, view):
        # To draw the texture parts of the ground
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(sg.findNode(self.model, 'ground'), pipeline_texture)
