from CourseResources import easy_shaders as es
from CourseResources import basic_shapes as bs
from CourseResources import scene_graph2 as sg
from CourseResources import transformations2 as tr
from OpenGL.GL import *


class End(object):

    def __init__(self):
        # Creation of basic figure of the end scene
        gpu_background_quad = es.toGPUShape(
            bs.createTextureQuad("/home/fabiwave/PycharmProjects/T1C-poke-snake/T1/MVC/Models/Images/end.png"),
            GL_REPEAT, GL_NEAREST)
        end_scene = sg.SceneGraphNode("End")
        end_scene.transform = tr.uniformScale(1)
        end_scene.childs += [gpu_background_quad]

        # Translation and scale of the end scene
        end_scene.transform = tr.matmul([tr.scale(2, 2, 1), tr.translate(0, 0, 1)])

        # Designation of the previous background as the model of this class
        self.model = end_scene

    # Draws the end node into the scene
    # TODO: Transform to 3D
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    # TODO: Revisar uso en 3d
    def rotate(self, angle):
        self.model.transform = tr.rotationZ(angle)