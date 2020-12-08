import os
import sys
from math import pi

import glfw
import pygame
from OpenGL.GL import *

from CourseResources import easy_shaders as es
from CourseResources import lighting_shaders as ls
from MVC.Controllers import Controller
from MVC.Models import Apple
from MVC.Models import Background
from MVC.Models import End
from MVC.Models import Snake
from MVC.Models import Wall
from MVC.Views.Camera import Camera


def run(grid_size=10):
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

    # Assembling the shader program (pipeline) with all of the necessary shaders
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimpleGouraudShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Activates the depth as we are working in 3D
    glEnable(GL_DEPTH_TEST)

    # Creation of the models
    real_grid_size = grid_size + 2
    last_move = 0.0
    apple = Apple.Apple(real_grid_size)
    snake = Snake.Snake(real_grid_size, apple)
    background = Background.Background(real_grid_size)
    wall = Wall.Wall(real_grid_size)
    end_scene = End.End()

    # Camera settings and projection
    camera = Camera(real_grid_size)

    # Models to control by the controller are set
    controller.set_snake(snake, camera)

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

        # Settings from the camera
        projection = camera.get_projection()
        view = camera.get_view(snake)

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
                    end_scene.rotate(pi / 8)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # We terminate the window
    glfw.terminate()
