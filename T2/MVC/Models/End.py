from OpenGL.GL import *

from CourseResources import basic_shapes as bs
from CourseResources import easy_shaders as es
from CourseResources import scene_graph2 as sg
from CourseResources import transformations2 as tr


class End(object):

    def __init__(self):
        # Creation of basic figure of the end scene
        gpu_end = es.toGPUShape(
            bs.createTextureCube("/home/fabiwave/PycharmProjects/T2C-PokeSnake3D/T2/MVC/Models/Images/end.png"),
            GL_REPEAT, GL_NEAREST)
        end_scene = sg.SceneGraphNode("End")
        end_scene.transform = tr.uniformScale(1)
        end_scene.childs += [gpu_end]

        # Translation and scale of the end scene
        end_scene.transform = tr.matmul([tr.translate(0, 0, 1), tr.scale(1.25, 1, 1)])

        # Designation of the previous background as the model of this class
        self.model = end_scene

    # Draws the end node into the scene
    def draw(self, pipeline_texture, projection, view):
        # To draw the texture parts of the snake
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_texture.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(sg.findNode(self.model, 'End'), pipeline_texture)

    def rotate(self, angle):
        self.model.transform = tr.matmul([self.model.transform, tr.rotationZ(angle)])
