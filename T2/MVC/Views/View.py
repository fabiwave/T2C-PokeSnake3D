import sys
import os
import glfw
import numpy as np
import pygame
from OpenGL.GL import *
from math import pi
from CourseResources import easy_shaders as es
from CourseResources import lighting_shaders as ls
from CourseResources import transformations2 as tr
from MVC.Controllers import Controller
from MVC.Models import Apple
from MVC.Models import Background
from MVC.Models import Snake
from MVC.Models import Wall
from MVC.Models import End

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
    # Setting up the view transform

    camera_theta = -3*pi/4
    R = 1
    camX = R * np.sin(camera_theta)
    camY = R * np.cos(camera_theta)
    viewPos = np.array([camX, camY, 1])
    view = tr.lookAt(
        viewPos,
        np.array([0, 0, 1]),
        np.array([0, 0, 1])
    )

    # Setting up the projection transform
    projection = tr.perspective(60, float(width) / float(height), 0.1, 10)

    view = tr.lookAt(  # Where to point and where is the camera
        np.array([10, 10, 5]),
        np.array([0, 0, 0]),
        np.array([0, 0, 1])
    )


    # Creation of the models
    size = 17
    last_move = 0.0
    apple = Apple.Apple(size)
    snake = Snake.Snake(size, apple)
    background = Background.Background(size)
    wall = Wall.Wall(size)
    end_scene = End.End()

    # Models to control by the controller are set
    controller.set_snake(snake)

    # Initializes pygame for music
    music_path = os.path.abspath(os.path.dirname(__file__))
    pygame.init()
    pygame.mixer.music.load(os.path.join(music_path, 'caminar.mp3'))
    pygame.mixer.music.play(-1, 0)
    game_over_time = 0

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

        # Movement of the snake
        current_time = glfw.get_time()
        time = 0.35
        delta = current_time - last_move

        # Time for update of movement
        if delta > time:
            snake.continue_move()
            last_move = glfw.get_time()

        # Handles the apple been eaten by snake
        snake.eat_apple()

        # Handles the snake collide against a wall
        if snake.wall_collision() or snake.snake_collision():
            end_scene.draw(textureShaderProgram, projection, view)
            if game_over_time == 0:
                game_over_time = glfw.get_time()
                pygame.mixer.music.load(os.path.join(music_path, 'game_over.mp3'))
                pygame.mixer.music.play(-1, 0)
            else:
                current_time = glfw.get_time()
                seconds = (current_time - game_over_time)
                if seconds > 0.475:
                    game_over_time = glfw.get_time()
                    end_scene.rotate(pi / 7)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # We terminate the window
    glfw.terminate()
