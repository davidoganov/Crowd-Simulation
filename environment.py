"""
Created on Mon May 22 2023

@author: HWM
"""
import numpy as np
from Agent import Agents

class Environment:
    """
    Class: Environment
    Description: This class represents the environment in the crowd evacuation simulation. 
                 It manages the grid, obstacles, exits, and provides utility methods to interact with the environment.

    Attributes:
        width (int): The width of the environment grid.
        height (int): The height of the environment grid.
        grid (np.ndarray): The 2D grid representing the environment.
        obstacles (List[Tuple[int, int]]): The positions of the obstacles in the environment.
        exits (List[Tuple[int, int]]): The positions of the exits in the environment.

    Methods:
        __init__(self, width, height): Initializes the Environment object with the specified width and height.
        is_obstacle(self, x, y): Checks if the given position is occupied by an obstacle.
        is_within_bounds(self, x, y): Checks if the given position is within the bounds of the environment.
        print_grid(self): Prints the grid representation of the environment.

    """

    def __init__(self, width: int, height: int):
        """
        Initialize the Environment object.

        Args:
            width (int): The width of the environment grid.
            height (int): The height of the environment grid.

        """
        self.width = width
        self.height = height
        self.grid = np.full((height, width), None)
        self.obstacles = []  # List to store obstacle positions
        self.exits = [(0, height-1), (width-1, 0)]  # Hardcoded exit positions

        for x, y in self.obstacles:
            obstacle = Agents.Obstacle(x, y)
            self.grid[y, x] = obstacle

        for x, y in self.exits:
            self.grid[y, x] = "Exit"

    def is_obstacle(self, x: int, y: int) -> bool:
        return self.grid[y, x] is not None

    def is_within_bounds(self, x: int, y: int) -> bool:
        """
        Check if the given position is within the bounds of the environment.

        Args:
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.

        Returns:
            bool: True if the position is within the bounds, False otherwise.

        """
        return 0 <= x < self.width and 0 <= y < self.height

    def print_grid(self):
        """
        Print the grid representation of the environment.

        """
        for row in self.grid:
            print(row)

