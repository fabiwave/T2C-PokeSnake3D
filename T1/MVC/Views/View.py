import os
import sys
import glfw
import pygame
from math import pi
from OpenGL.GL import *
from CourseResources import easy_shaders as es
from MVC.Models import Snake
from MVC.Models import Background
from MVC.Models import Wall
from MVC.Models import Apple
from MVC.Models import End
from MVC.Controllers import Controller


def run(grid_size=10):
    last_move = 0.0

    # We initialize glfw
    if not glfw.init():
        sys.exit()

    # Set width and height of the window
    width = 800
    height = 800

    # We create the window with the previous params
    window = glfw.create_window(width, height, 'Poke-Snake', None, None)

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

    # Assembling the shader program (pipeline) with both shaders
    pipeline_color = es.SimpleTransformShaderProgram()
    pipeline_texture = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline_texture.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creation of the models
    real_grid_size = grid_size + 2
    wall = Wall.Wall(real_grid_size)
    apple = Apple.Apple(real_grid_size)
    snake = Snake.Snake(real_grid_size, apple)
    background = Background.Background()
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
        glClear(GL_COLOR_BUFFER_BIT)

        # Draws the nodes of the scene
        background.draw(pipeline_texture)
        wall.draw(pipeline_texture)
        snake.draw(pipeline_texture)
        apple.draw(pipeline_color)

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
            end_scene.draw(pipeline_texture)
            if game_over_time == 0:
                game_over_time = glfw.get_time()
                pygame.mixer.music.load(os.path.join(music_path, 'game_over.mp3'))
                pygame.mixer.music.play(-1, 0)
            else:
                current_time = glfw.get_time()
                end_scene.rotate((current_time - game_over_time) * pi / 8)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # We terminate the window
    glfw.terminate()
