import numpy as np
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, width: int, height: int):
        """
        Initializes a new instance of the Environment class.

        Args:
            width (int): The width of the environment grid.
            height (int): The height of the environment grid.
        """
        self.width = width
        self.height = height
        self.grid = np.full((height, width), None)
        self.obstacles = set()
        self.exits = []
        self.persons = []
        self.fires = []

    def add_obstacle(self, x: int, y: int):
        """
        Adds an obstacle at the specified position in the environment.

        Args:
            x (int): The x-coordinate of the obstacle position.
            y (int): The y-coordinate of the obstacle position.
        """
        self.obstacles.add((x, y))
        self.grid[y, x] = "Obstacle"

    def add_exit(self, x: int, y: int):
        """
        Adds an exit at the specified position in the environment.

        Args:
            x (int): The x-coordinate of the exit position.
            y (int): The y-coordinate of the exit position.
        """
        self.exits.append((x, y))
        self.grid[y, x] = "Exit"

    def add_person(self, person):
        """
        Adds a person to the environment.

        Args:
            person (Person): The Person object to be added.
        """
        self.persons.append(person)

    def add_fire(self, fire):
        """
        Adds a fire at the specified position in the environment.

        Args:
            fire (Fire): The Fire object to be added.
        """
        for existing_fire in self.fires:
            if (existing_fire.xPos, existing_fire.yPos) == (fire.xPos, fire.yPos):
                return  # Do not add fire if a fire already exists at the same position
        self.fires.append(fire)
        self.grid[fire.yPos, fire.xPos] = "Fire"

    def is_fire(self, x: int, y: int) -> bool:
        """
        Checks if the specified position in the environment is a fire.

        Args:
            x (int): The x-coordinate of the position to check.
            y (int): The y-coordinate of the position to check.

        Returns:
            bool: True if the position is a fire, False otherwise.
        """
        for fire in self.fires:
            if (fire.xPos, fire.yPos) == (x, y):
                return True
        return False

    def is_obstacle(self, x: int, y: int) -> bool:
        """
        Checks if the specified position in the environment is an obstacle.

        Args:
            x (int): The x-coordinate of the position to check.
            y (int): The y-coordinate of the position to check.

        Returns:
            bool: True if the position is an obstacle, False otherwise.
        """
        return (x, y) in self.obstacles

    def is_within_bounds(self, x: int, y: int) -> bool:
        """
        Checks if the specified position is within the bounds of the environment.

        Args:
            x (int): The x-coordinate of the position to check.
            y (int): The y-coordinate of the position to check.

        Returns:
            bool: True if the position is within the environment bounds, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def plot(self, agents):
        """
        Plots the environment grid with agents and objects.

        Args:
            agents (Agents): The Agents object containing the agents and objects to be plotted.
        """
        fig, ax = plt.subplots()

        for exit in self.exits:
            ax.scatter(*exit, color='green', label='Exit')

        for obstacle in self.obstacles:
            ax.scatter(*obstacle, color='black', label='Obstacle')

        for person in agents.persons:
            ax.scatter(person.xPos, person.yPos, color='blue', label='Person')

        for fire in agents.fires:
            ax.scatter(fire.xPos, fire.yPos, color='red', label='Fire')

        ax.set_xticks(np.arange(0, self.width, 1))
        ax.set_yticks(np.arange(0, self.height, 1))
        ax.grid(True)
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()
