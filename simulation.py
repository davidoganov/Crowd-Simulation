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
        self.agents = Agents(environment, num_people, num_fires)
        self.timestep = 0
        self.escaped_counts = []
        self.escaped_persons = []

        
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
                    elif 3 <= person.panic < 7:  # Moderate panic level: try to stay near others but still aim for the least congested exit
                        person.move_towards_least_congested_exit(consider_others=True)
                    else:  # High panic level: follow the crowd
                        person.follow_crowd(self.agents.persons)
            # After updating each person's state, update the environment.
            self.agents.environment.add_person(person)


            if person.is_escaped(self.timestep):
                person.time_to_escape = self.timestep
                self.escaped_persons.append(person)
            elif person.is_dead():
                print(f"Person at ({person.xPos}, {person.yPos}) has died!")
            else:
                surviving_people.append(person)  # Only add person to new list if they are not dead or escaped
                
        self.timestep += 1
        self.agents.persons = surviving_people  # Replace old list with new one
        self.escaped_counts.append(len(self.escaped_persons))  # Record the number of escaped people



        escape_times = [p.time_to_escape for p in self.escaped_persons]
        num_escaped = len(self.escaped_persons)
            
        
        # Print the results
        print(f"Number of people who escaped: {num_escaped}")
        if num_escaped > 0:
            print(f"Average escape time: {sum(escape_times) / num_escaped}")
            print(f"Minimum escape time: {min(escape_times)}")
            print(f"Maximum escape time: {max(escape_times)}")
            
        

        for fire in self.agents.fires:
            fire.fire_spread()
            fire.calculate_effect(self.agents.persons)
            # After updating each fire's state, update the environment.
            self.agents.environment.add_fire(fire)
