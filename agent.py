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
        self.panic_levels = []
        self.dead = 0

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
            
    def update(self):
        # Update state of each person
        for person in self.persons:
            person.update_panic()
            person.move_towards_least_congested_exit(consider_others=True)
            person.follow_crowd(self.persons)
            self.panic_levels.append(person.panic)

        # Update state of each fire
        for fire in self.fires:
            fire.fire_spread()
            fire.calculate_effect(self.persons)
                
    class Person:
        """
        Represents a person in the simulation.
        """

        panic = 0
        health = 50

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
            self.social_distance = 5
            self.congestion_radius = 10  # consider persons within a distance of 10 as contributing to congestion
            


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
            print(f'Person moved to: ({self.xPos}, {self.yPos})')


        def move_towards_least_congested_exit(self, consider_others=False):
            least_congested_exit = None
            least_congestion = float('inf')

            # Calculate congestion for each exit
            for exit in self.environment.exits:
                congestion = sum(1 for person in self.environment.persons if self.distance_to(person) <= self.congestion_radius)
                if congestion < least_congestion:
                    least_congestion = congestion
                    least_congested_exit = exit

            if consider_others:
                # Try to stay close to others while moving towards the exit
                nearest_person = min((person for person in self.environment.persons if person != self),
                                 key=self.distance_to, default=None)
                if nearest_person is not None and self.distance_to(nearest_person) > self.social_distance:
                    self.move_towards(nearest_person)
                    return

            # Move towards the least congested exit
            if least_congested_exit is not None:
                self.move_towards(least_congested_exit)
        
        def distance_to(self, other):
            return ((self.xPos - other.xPos)**2 + (self.yPos - other.yPos)**2)**0.5

        def move_towards(self, position):
            # Check if position is a Person instance or a tuple
            if isinstance(position, Agents.Person):
                dx = position.xPos - self.xPos
                dy = position.yPos - self.yPos
            else:
                dx = position[0] - self.xPos
                dy = position[1] - self.yPos

            distance = np.sqrt(dx**2 + dy**2)

            if distance > 0:
                dx /= distance
                dy /= distance

            new_x = int(self.xPos + dx)
            new_y = int(self.yPos + dy)

            if self.environment.is_within_bounds(new_x, new_y) and \
                not self.environment.is_obstacle(new_x, new_y):
                    self.xPos, self.yPos = new_x, new_y



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
            if self.health <= 0:
                self.dead += 1
                return True
            else:
                return False

        def is_escaped(self, timestep) -> bool:
            if (self.xPos, self.yPos) in self.environment.exits and self.time_to_escape is None:
                self.escaped = True
                self.time_to_escape = timestep
                return True
            else:
                return False

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
