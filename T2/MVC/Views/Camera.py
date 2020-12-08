import numpy as np

from CourseResources import transformations2 as tr


class Camera(object):

    def __init__(self, grid_size):
        self.grid_unit = 2 / grid_size
        self.current_mode = "person"

    # Returns the view related to a kind of camera
    def get_view(self, snake):
        if self.current_mode == "person":
            view = self.get_first_person_view(snake)
        elif self.current_mode == "2d":
            view = self.get_2d_view()
        elif self.current_mode == "perspective":
            view = self.get_perspective_view()
        return view

    # Returns the projection related to a kind of camera
    def get_projection(self):
        if self.current_mode == "person":
            projection = self.get_first_person_projection()
        elif self.current_mode == "2d":
            projection = self.get_2d_projection()
        elif self.current_mode == "perspective":
            projection = self.get_perspective_projection()
        return projection

    # Returns the view of a 2d camera
    def get_2d_view(self):
        view = tr.lookAt(
            np.array([self.grid_unit, self.grid_unit, 1 + self.grid_unit]),
            np.array([self.grid_unit, self.grid_unit, 0]),
            np.array([0, 1, 1]))
        return view

    # Returns the projection of a 2d camera
    def get_2d_projection(self):
        projection = tr.ortho(-1 - self.grid_unit, 1 + self.grid_unit, -1 - self.grid_unit, 1 + self.grid_unit,
                              0.1, 100)
        return projection

    # Sets the camera with a perspective vision
    def get_perspective_view(self):
        view = tr.lookAt(
            np.array([-1, -1, 1 + self.grid_unit]),
            np.array([0, 0, 0]),
            np.array([1, 1, 1]))
        return view

    # Returns the projection of a 2d camera
    @staticmethod
    def get_perspective_projection():
        projection = tr.perspective(90, 1, 0.1, 10)
        return projection

    # Returns the view of a first person camera
    def get_first_person_view(self, snake):
        last_mov = snake.get_head_last_mov()
        snake_pos = snake.get_position()

        # View settings
        eye_x = snake_pos[0]
        eye_y = snake_pos[1]
        at_x = snake_pos[0]
        at_y = snake_pos[1]

        if last_mov == "Up":
            at_y = 1
        elif last_mov == "Down":
            at_y = -1
        elif last_mov == "Right":
            at_x = 1
        elif last_mov == "Left":
            at_x = -1

        view = tr.lookAt(
            np.array([eye_x, eye_y, self.grid_unit]),
            np.array([at_x, at_y, self.grid_unit]),
            np.array([0, 0, self.grid_unit]))
        return view

    # Returns the projection of a first person camera
    def get_first_person_projection(self):
        projection = tr.frustum(-self.grid_unit, self.grid_unit, -self.grid_unit, self.grid_unit, 0.1, 100)
        return projection

    # Sets the current mode as a 2d camera
    def set_2d_camera(self):
        self.current_mode = "2d"

    # Sets the current mode as a perspective camera
    def set_perspective_camera(self):
        self.current_mode = "perspective"

    # Sets the current mode as a first person camera
    def set_first_person_camera(self):
        self.current_mode = "person"

    # Returns the current mode of the camera
    def get_current_mode(self):
        return self.current_mode
