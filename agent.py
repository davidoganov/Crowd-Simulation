import numpy as np
import random as random

class Agents:
    """
    Represents the collection of agents in the simulation.
    """

    def __init__(self, env, num_people, num_fires):
        """
        Initializes the Agents object with the specified environment, number of people, and number of fires.

        Args:
            env (Environment): The environment in which the agents operate.
            num_people (int): The number of people in the simulation.
            num_fires (int): The number of fires in the simulation.
        """
        self.environment = env
        self.persons = []
        self.fires = []
        self.obstacles = []
        self.exits = []

        # Generate random positions for people
        for _ in range(num_people):
            person = self.Person(random.randint(0, env.width - 1), random.randint(0, env.height - 1), self.environment)
            self.persons.append(person)
            self.environment.add_person(person)

        # Generate random positions for fires
        for _ in range(num_fires):
            fire = self.Fire(random.randint(0, env.width - 1), random.randint(0, env.height - 1), self.environment)
            self.fires.append(fire)
            self.environment.add_fire(fire)

    class Person:
        """
        Represents a person in the simulation.
        """

        panic = 0
        health = 200

        def __init__(self, xPos: int, yPos: int, env):
            """
            Initializes the Person object with the specified position and environment.

            Args:
                xPos (int): The x-coordinate of the person's position.
                yPos (int): The y-coordinate of the person's position.
                env (Environment): The environment in which the person operates.
            """
            self.environment = env
            self.xPos = xPos
            self.yPos = yPos
            self.escaped = False
            self.time_to_escape = None  # None means person has not escaped yet


        def update_panic(self):
            """
            Updates the panic level of the person based on their proximity to fires.
            """
            for fire in self.environment.fires:
                if np.sqrt((fire.xPos - self.xPos) ** 2 + (fire.yPos - self.yPos) ** 2) < 3:
                    self.panic += 1
                    return
            self.panic = max(0, self.panic - 1)

        def can_move(self, dx: int, dy: int) -> bool:
            """
            Checks if the person can move in the specified direction.

            Args:
                dx (int): The change in the x-coordinate.
                dy (int): The change in the y-coordinate.

            Returns:
                bool: True if the person can move, False otherwise.
            """
            return self.environment.is_within_bounds(self.xPos + dx, self.yPos + dy) and \
                   not self.environment.is_obstacle(self.xPos + dx, self.yPos + dy)

        def move(self, dx: int, dy: int):
            """
            Moves the person in the specified direction if possible.

            Args:
                dx (int): The change in the x-coordinate.
                dy (int): The change in the y-coordinate.
            """
            if self.can_move(dx, dy):
                self.xPos += dx
                self.yPos += dy

        def move_towards_least_congested_exit(self):
            """
            Moves the person towards the least congested exit.
            """
            exits_with_congestion = [(exit, sum(np.sqrt((p.xPos - exit[0]) ** 2 + (p.yPos - exit[1]) ** 2) < 5 for p in self.environment.persons)) for exit in self.environment.exits]
            least_congested_exit = min(exits_with_congestion, key=lambda e: e[1])[0]
            dx = np.sign(least_congested_exit[0] - self.xPos)
            dy = np.sign(least_congested_exit[1] - self.yPos)
            self.move(dx, dy)

        def follow_crowd(self, persons):
            """
            Moves the person in the direction of the average movement of nearby persons.

            Args:
                persons (list): The list of all persons in the simulation.
            """
            if len(persons) > 1:
                directions = [(p.xPos - self.xPos, p.yPos - self.yPos) for p in persons if p != self]
                avg_direction = (np.mean([d[0] for d in directions]), np.mean([d[1] for d in directions]))
                dx = np.sign(avg_direction[0])
                dy = np.sign(avg_direction[1])
                self.move(dx, dy)

        def is_dead(self) -> bool:
            """
            Checks if the person is dead.

            Returns:
                bool: True if the person is dead, False otherwise.
            """
            return self.health <= 0

        def escaped(self, timestep) -> bool:
            if (self.xPos, self.yPos) in self.environment.exits and self.time_to_escape is None:
                self.escaped = True
                self.time_to_escape = timestep
            return self.is_escaped

    class Fire:
        """
        Represents a fire in the simulation.
        """

        def __init__(self, xPos: int, yPos: int, environment):
            """
            Initializes the Fire object with the specified position and environment.

            Args:
                xPos (int): The x-coordinate of the fire's position.
                yPos (int): The y-coordinate of the fire's position.
                environment (Environment): The environment in which the fire exists.
            """
            self.xPos = xPos
            self.yPos = yPos
            self.environment = environment

        def fire_spread(self):
            """
            Spreads the fire to neighboring cells in a randomized manner.
            """
            spread_probability = 0.2  # Only a 20% chance for fire to spread to a neighboring cell
            directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x = self.xPos + dx
                new_y = self.yPos + dy
                if (self.environment.is_within_bounds(new_x, new_y) and 
                    not self.environment.is_obstacle(new_x, new_y) and 
                    not self.environment.is_fire(new_x, new_y)):
                    if random.random() < spread_probability:  # Use a random number to decide whether to spread
                        new_fire = Agents.Fire(new_x, new_y, self.environment)
                        self.environment.add_fire(new_fire)
                        return


        def calculate_effect(self, persons):
            """
            Calculates the effect of the fire on nearby persons' health.
            """
            for person in persons:
                distance = np.sqrt((person.xPos - self.xPos) ** 2 + (person.yPos - self.yPos) ** 2)
                if distance < 3:  # Fire affects person if they are within 3 units
                    person.health -= 1  # Fire decreases health by 1 unit
                elif distance < 5:  # Fire affects person if they are within 5 units, but less so than if they are within 3 units
                    person.health -= 0.5  # Fire decreases health by 0.5 units

