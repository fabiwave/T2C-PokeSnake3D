import sys

import glfw


class Controller(object):

    def __init__(self):
        self.snake = None

    def set_snake(self, snake):
        self.snake = snake

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and action == glfw.PRESS:
            self.snake.set_last_move("Left")

        elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and action == glfw.PRESS:
            self.snake.set_last_move("Right")

        elif (key == glfw.KEY_UP or key == glfw.KEY_W) and action == glfw.PRESS:
            self.snake.set_last_move("Up")

        elif (key == glfw.KEY_DOWN or key == glfw.KEY_S) and action == glfw.PRESS:
            self.snake.set_last_move("Down")

        else:
            return

