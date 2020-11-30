import sys

import glfw
import numpy as np
from OpenGL.GL import *

from CourseResources import easy_shaders as es
from CourseResources import lighting_shaders as ls
from CourseResources import transformations2 as tr
from MVC.Controllers import Controller
from MVC.Models import Apple
from MVC.Models import Background
from MVC.Models import Snake
from MVC.Models import Wall

if __name__ == '__main__':
    # We initialize glfw
    if not glfw.init():
        sys.exit()

    # Set width and height of the window
    width = 800
    height = 800

    # We create the window with the previous params
    window = glfw.create_window(width, height, 'Poke-Snake 3D', None, None)

    # Handle the exception of the window not been created properly
    if not window:
        glfw.terminate()
        sys.exit()

    # Set the window as the current window
    glfw.make_context_current(window)

    # Set the controller
    controller = Controller.Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Assembling the shader program (pipeline) with all of the necesary shaders
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimpleGouraudShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Activates the depth as we are working in 3D
    glEnable(GL_DEPTH_TEST)

    # Camera settings and projection
    projection = tr.ortho(-2, 2, -2, 2, 0.1, 1000)  # Visualization volume
    view = tr.lookAt(  # Where to point and where is the camera
        np.array([10, 10, 5]),
        np.array([0, 0, 0]),
        np.array([0, 0, 1])
    )

    size = 17

    # Creation of the models
    apple = Apple.Apple(size)
    snake = Snake.Snake(size, apple)
    background = Background.Background(size)
    wall = Wall.Wall(size)

    # Models to control by the controller are set
    controller.set_snake(snake)

    # Game logic to play the Snake
    while not glfw.window_should_close(window):
        # We obtain the events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # We draw the models into the scene
        wall.draw(textureShaderProgram, projection, view)
        snake.draw(textureShaderProgram, projection, view)
        background.draw(textureShaderProgram, projection, view)
        apple.draw(lightShaderProgram, projection, view)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # We terminate the window
    glfw.terminate()
