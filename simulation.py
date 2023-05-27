import numpy as np
from agent import Agents
from environment import Environment

class Simulation:
    """
    Represents the simulation of the environment with agents.
    """

    def __init__(self, env_width, env_height, num_people, num_fires, num_obstacles, exit_positions):
        """
        Initializes the Simulation object with the specified parameters.

        Args:
            env_width (int): The width of the environment.
            env_height (int): The height of the environment.
            num_people (int): The number of people in the simulation.
            num_fires (int): The number of fires in the simulation.
            num_obstacles (int): The number of obstacles in the environment.
            exit_positions (list): A list of tuples representing the positions of exits.
        """
        environment = Environment(env_width, env_height)
        for pos in exit_positions:
            environment.add_exit(*pos)
        self.agents = Agents(environment, num_people, num_fires)
        self.timestep = 0
        self.escaped_counts = []

        # Generate random positions for people
        for i in range(num_people):
            x, y = np.random.randint(0, env_width), np.random.randint(0, env_height)
            self.agents.persons.append(Agents.Person(x, y, self.agents.environment))

        # Generate random positions for fires
        for i in range(num_fires):
            x, y = np.random.randint(0, env_width), np.random.randint(0, env_height)
            self.agents.fires.append(Agents.Fire(x, y, environment))

        # Generate random positions for obstacles
        for i in range(num_obstacles):
            x, y = np.random.randint(0, env_width), np.random.randint(0, env_height)
            environment.add_obstacle(x, y)

        # Add exits to the environment
        for exit in exit_positions:
            environment.add_exit(*exit)

    def step(self):
        """
        Performs a single step in the simulation, updating the positions and states of the agents.
        """
        surviving_people = []  # Create a new list for people who are still alive

        for person in self.agents.persons:
            person.update_panic()
            if not person.is_dead():
                if not person.escaped:
                    if person.panic < 3:
                        person.move_towards_least_congested_exit()
                    else:
                        person.follow_crowd(self.agents.persons)

            if person.escaped:
                print(f"Person at ({person.xPos}, {person.yPos}) has escaped!")
                person.time_to_escape = self.timestep
            elif person.is_dead():
                print(f"Person at ({person.xPos}, {person.yPos}) has died!")
            else:
                surviving_people.append(person)  # Only add person to new list if they are not dead or escaped
                
        self.timestep += 1
        self.escaped_counts.append(len([person for person in self.agents.persons if person.escaped]))  # Record the number of escaped people

        escaped_people = [person for person in self.agents.persons if person.escaped]
        escape_times = [p.time_to_escape for p in self.agents.persons if p.time_to_escape is not None]
        num_escaped = len(escape_times)

        # Print the results
        print(f"Number of people who escaped: {num_escaped}")
        if num_escaped > 0:
            print(f"Average escape time: {sum(escape_times) / num_escaped}")
            print(f"Minimum escape time: {min(escape_times)}")
            print(f"Maximum escape time: {max(escape_times)}")
            
        self.agents.persons = surviving_people  # Replace old list with new one

        for fire in self.agents.fires:
            fire.fire_spread()
            fire.calculate_effect(self.agents.persons)
