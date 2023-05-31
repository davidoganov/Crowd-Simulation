from simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np
import random as random
import time

def main():
    env_height = 20
    env_width = 20
    num_fires = 3
    num_obstacles = 5
    exitPos1 = (1, 1)
    exitPos2 = (19, 19)
    simulations = 10
    persons = 10
    timeStep = 10
    
    """    Average Number of Escaped Persons over Grid Sizes      """
    plot_various_grid_sims(simulations, timeStep, persons, num_fires, num_obstacles)
    
    """    proj-escaped vs. actual     """
    plot_proj_num_escaped_vs_actual(simulations, timeStep, env_height, env_width, persons,
                                    num_fires, num_obstacles, exitPos1, exitPos2)
    
    """    number of people escaped over time     """
    calculate_and_plot_num_escaped_over_time(simulations, timeStep, env_width, env_height,
                                             persons, num_fires, num_obstacles, exitPos1, exitPos2)
    
    """    different exit door positions and numbers of exits and calculates the average escape counts and standard deviations for each combination      """
    calculate_and_plot_exit_variation(simulations, timeStep, env_width, env_height, 
                                      persons, num_fires, num_obstacles)
        
    """    dead over time      """
    calculate_and_plot_dead_over_time(simulations, timeStep, env_width, env_height, persons,
                                      num_fires, num_obstacles, exitPos1, exitPos2)
   
    """    bottlenecks vs # of ppl OR exits      """
    bottleneck_plot()

    
# end main


def run_simulation(simulation, timeStep):
    """
    Runs the simulation using the provided simulation instance, and specified timeStep
    Args:
        simulations (Simulation): The instance of the simulation to run
        timeStep (int): Thhe number of seconds the persons in the room have to escape
        
    Returns: plt - Plot of the simulation (1 frame per timeStep)
            timeSteps - List of timestep values used to plot in several functions
    """
    
    # print out the parameters being used in the simulation 
    print("=========================================================================")
    print(f"Number of persons in Simulation: {len(simulation.agents.persons)}")
    print(f"Number of fires in Simulation: {len(simulation.agents.fires)}")
    print(f"Number of obstacles in Simulation: {simulation.obstacle_count}")
    print(f"Time step being used in the Simulation: {(timeStep)}")
    print("=========================================================================")
    
    # init list of time steps
    timeSteps = []
    
    # loop thru the specified number of time steps
    for step in range(timeStep): 
        # step thru the simulation
        simulation.step()
        
        # plot the environment
        simulation.agents.environment.plot(simulation.agents)
        
        # add the timestep to the list
        timeSteps.append(step)
        print(f"----------------------  Time Step {step + 1} Completed  ----------------------")
    print(f"-------------------  Simulation Run #{timeStep} Completed  -------------------")
    print(" ")
    return timeSteps
        

def proj_num_escaped(simulations, timeStep, env_height, env_width, persons, num_fires, num_obstacles, exitPos1, exitPos2):
    """
    Calculates and returns the projected number of escapees from the simulation: 
        Sums the entirety of the escapees from a variable simulation number 
            (recommended at least double plot amount) 
        calculates the average number of escapees from the simulations
    Args:
        simulations (int): The number of simulations to run
        timeStep (int): The number of seconds the persons in the room have to escape
        env_height (int): The height of the environment grid
        env_width (int): The width of the environment grid
        persons (int): The number of persons in the environment grid
        num_fires (int): The number of fires in the environment grid
        num_obstacles (int): The number of obstacles in the environment grid
        exitPos1 (tuple): The coordinates of the first exit door in the environment grid
        exitPos2 (tuple): The coordinates of the second exit door in the environment grid
    
    Returns: proj_avg_escapees - the projected average number of persons escaped from the room
    """
    
    # init escapee count
    escapees = 0 
    
    # loop through the number of simulations
    for i in range(simulations): 
        # set the simulation environment
        simulation = Simulation(env_height, env_width, persons, num_fires, num_obstacles, [exitPos1, exitPos2]) 
    
        # loop through each time step
        run_simulation(simulation, timeStep)
    
        # add the number escaped in the current simulation to running total
        escapees += simulation.num_escaped  
        
    # break for 2 seconds    
    time.sleep(2)
    
    # calculate the average number escaped in all simulations
    proj_avg_escapees = escapees / simulations 
    return proj_avg_escapees

def plot_proj_num_escaped_vs_actual(simulations, timeStep, env_height, env_width, persons, num_fires, num_obstacles, exitPos1, exitPos2):
    """
    Runs the simulation a given number of times, calculating the actual number of escapees
        and plots that against the calculated projected average number of escapees 
    Args:
        simulations (int): The number of simulations to run
        timeStep (int): The number of seconds the persons in the room have to escape
        env_height (int): The height of the environment grid
        env_width (int): The width of the environment grid
        persons (int): The number of persons in the environment grid
        num_fires (int): The number of fires in the environment grid
        num_obstacles (int): The number of obstacles in the environment grid
        exitPos1 (tuple): The coordinates of the first exit door in the environment grid
        exitPos2 (tuple): The coordinates of the second exit door in the environment grid
    
    Returns: plt - Plot of Projected Escapees vs. Actual Escapees for a given number of simulation iterations
    """
    
    # calculate the projected avg number of escapees
    proj_escape_num = proj_num_escaped(simulations, timeStep, env_height, env_width,
                                       persons, num_fires, num_obstacles, exitPos1, exitPos2)
    actual_escape_counts = []
    
    # loop thru simulations 
    for i in range(simulations):
        # set the simulation environment
        simulation = Simulation(env_height, env_width, persons, num_fires, num_obstacles, [exitPos1, exitPos2]) 
        
        # loop thru each time step of the simulation
        run_simulation(simulation, timeStep)
        # add the number of escapees  in the current simulation to list
        actual_escape_counts.append(simulation.num_escaped) 
        print(f"Completed Simulation Run #{i + 1}")
        
    # break for 2 seconds    
    time.sleep(2)
    
    # create x-axis values to be simulation iterations 1 to 10
    x = range(1, simulations + 1)
    
    # duplicate projected escape count to match length of actual_escape_counts
    proj_escape_num = [proj_escape_num] * len(x)
    
    # plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, proj_escape_num, label='Projected Escapees', linestyle='--', color='blue', marker='o')
    plt.plot(x, actual_escape_counts, label='Actual Escapees', linestyle='-', color='red', marker='o')
    plt.xlabel('Simulation Time Step')
    plt.ylabel('Number of Escapees')
    plt.title(f'Projected Escapees vs Actual Escapees [{simulations} Simulations]')
    plt.legend()
    plt.show()

def calculate_and_plot_num_escaped_over_time(simulations, timeStep, env_width, env_height, num_people, num_fires, num_obstacles, exitPos1, exitPos2):
    """
    Runs the simulation a given number of times, calculating the time that it took
        persons to escape from the room in the environment grid.
    Args:
        simulations (int): The number of simulations to run
        timeStep (int): The number of seconds the persons in the room have to escape
        env_height (int): The height of the environment grid
        env_width (int): The width of the environment grid
        persons (int): The number of persons in the environment grid
        num_fires (int): The number of fires in the environment grid
        num_obstacles (int): The number of obstacles in the environment grid
        exitPos1 (tuple): The coordinates of the first exit door in the environment grid
        exitPos2 (tuple): The coordinates of the second exit door in the environment grid
    
    Returns: plt - Plot of Projected Escapees vs. Actual Escapees for a given number of simulation iterations
    """
    
    # loop thru given number of simulations
    for i in range(simulations):
        # set simulation environment
        simulation = Simulation(env_width, env_height, num_people, num_fires, num_obstacles, [(exitPos1), (exitPos2)]) 
        
        # loop thru each time step in the simulation
        run_simulation(simulation, timeStep)
        
    # break for 2 seconds    
    time.sleep(2)
    
    # plot
    plt.plot(simulation.escaped_counts)
    plt.xlabel('Time step (seconds)')
    plt.ylabel('Number of escaped people')
    plt.title(f'Number of escaped people over {simulations} simulations')
    plt.show()
    
def calculate_and_plot_exit_variation(simulations, timeStep, env_width, env_height, persons, num_fires, num_obstacles):
    """
    performs the simulation with different exit door positions and numbers of exits and calculates the average escape counts and standard deviations for each combination:
    
    Args:
        simulations (int): The number of simulations to run
        timeStep (int): The number of seconds the persons in the room have to escape
        env_width (int): The width of the environment grid
        env_height (int): The height of the environment grid
        persons (int): The number of persons in the environment grid
        num_fires (int): The number of fires in the environment grid
        num_obstacles (int): The number of obstacles in the environment grid
    
    Returns: plt - Plot of Average Escape Counts with Standard Deviation
    
    """
    
    # init lists to record escape counts/positions, averages, and standard deviations
    esc_counts = []
    avg_escape_counts = []
    std_escape_counts = []
    rec_exit_locs = []
    
    # loop thru the specified number of simulation iterations
    for i in range(simulations):
        # obtain a random coordinate from the grid
        rand_coord = random.randint(env_height - env_width + 1, env_height - 1)
        
        # put together the two new exit location positions
        exit_locs = [(env_height - env_width + 1, rand_coord), (rand_coord, env_height - 1)]
        
        # create a simulation instance with the specified parameters and new exit positions
        sim = Simulation(env_width, env_height, persons, num_fires, num_obstacles, exit_locs)
        
        # run the simulation instance created above using the specified number of timeSteps
        run_simulation(sim, timeStep)
        
        # add the new exit locations for record
        rec_exit_locs.append(exit_locs)
        # add the number of escapees in the current simulation run
        esc_counts.append(sim.num_escaped)

        # calculate the avg of the number of escapees in the current simulation run
        avg_escape_count = np.mean(esc_counts)
        
        # calculate the standard deviation of the number of escapees in the current simulation run
        std_escape_count = np.std(esc_counts)
        
        # add that average to the list of averages
        avg_escape_counts.append(avg_escape_count)
        
        # add that standard deviation to the list of standard deviations
        std_escape_counts.append(std_escape_count)
        
    # break for 2 seconds    
    time.sleep(2)
    
    # plotting
    # change length of x to match rec_exit_locs
    x = np.arange(len(rec_exit_locs))  
    width = 0.35
    
    # adjust figure size to fit everything
    fig, ax = plt.subplots(figsize=(15, 6))  
    rects1 = ax.bar(x, avg_escape_counts, width, label='Average Escape Counts', yerr=std_escape_counts)
    
    ax.set_xlabel('Exit Configurations')
    ax.set_ylabel('Escape Counts')
    ax.set_title('Average Escape Counts with Standard Deviation')
    ax.set_xticks(x)
    ax.set_xticklabels([', '.join([str(pos) for pos in ep]) for ep in rec_exit_locs], rotation='horizontal')  # Simplify x-axis tick labels
    ax.legend()
    
    plt.tight_layout()
    plt.show()
    
def calculate_and_plot_dead_over_time(simulations, timeStep, env_width, env_height, persons, num_fires, num_obstacles, exitPos1, exitPos2):
    """
    Performs the simulation with the specified parameters and calculates the number of dead persons over time.
    Plots the number of dead persons over time.
    
    Args:
        simulations (int): The number of simulation iterations to run.
        timeStep (int): The number of seconds the persons in the room have to escape.
        env_width (int): The width of the simulation environment.
        env_height (int): The height of the simulation environment.
        persons (int): The number of persons in the simulation.
        num_fires (int): The number of fires in the simulation.
        num_obstacles (int): The number of obstacles in the simulation.
        exitPos1 (tuple): The position of the first exit (x, y).
        exitPos2 (tuple): The position of the second exit (x, y).
    """
    
    # list to store the num of dead persons at each time step
    dead_counts = []  
    
    # loop thru number of specified simulations
    for i in range(simulations):
        # create a simulation instance with the specified parameters
        sim = Simulation(env_width, env_height, persons, num_fires, num_obstacles, [exitPos1, exitPos2])
        
        # run the simulation for the specified time step
        run_simulation(sim, timeStep)
        print(f"Completed Simulation Run #{i + 1}")
        
        # get the number of dead persons at each time step & add it to the list
        dead_counts.append(abs(len(sim.agents.persons) - sim.num_escaped))
        print(f"List of dead counts = {dead_counts}")
    
    # break for 2 seconds    
    time.sleep(2)
    
    # plot the number of dead persons over time
    plt.plot(range(simulations), dead_counts)
    plt.xlabel('Simulation Iteration')
    plt.ylabel('Number of Dead Persons')
    plt.title('Number of Dead Persons Over Simulations')
    plt.tight_layout()
    plt.show()
    
def plot_various_grid_sims(simulations, timeStep, persons, num_fires, num_obstacles):
    """
    Runs simulations with various grid sizes and plots the average num_escaped over grid sizes.

    Args:
        simulations (int): The number of times to run the simulation.
        timeStep (int): The number of seconds the persons in the room have to escape.
        persons (int): The number of people in the simulation.
        num_fires (int): The number of fires in the simulation.
        num_obstacles (int): The number of obstacles in the simulation.
        exitPos1 (tuple): The position of the first exit as a tuple (x, y).
        exitPos2 (tuple): The position of the second exit as a tuple (x, y).
        
    Returns: plt - Plot of the average number of escaped persons over varying grid sizes
    """
    
    # grid sizes to test, increasing by 5 each time 10 - 30
    grid_sizes = range(10, 35, 5)  
    
    # init list to store average num_escaped for each grid size
    avg_num_escaped = []  

    # loop thru each grid size
    for grid_size in grid_sizes:
        # init list to store num_escaped for each simulation iteration
        escaped_counts = []  
        
        # get two random numbers to represent exit positions
        rand_coordX = random.randint(1, grid_size - 1)
        rand_coordY = random.randint(1, grid_size - 1 )     
        
        # loop thru specified number of simulations
        for _ in range(simulations):
            print(f"Grid size being used: {grid_size}")
            
            # init new simulation instance for each iteration
            simulation = Simulation(grid_size, grid_size, persons, num_fires, num_obstacles, [(1, rand_coordY), (grid_size - 1, rand_coordX)])
                        
            # run the sim
            run_simulation(simulation, timeStep)
            
            # store the num_escaped for current sim
            escaped_counts.append(simulation.num_escaped)
            
        # calculate average num_escaped for current grid size
        avg_num_escaped.append(sum(escaped_counts) / simulations)
    
    print(f"Total number of simulations performed at each grid size: {simulations}")
    print(f"Total number of grid sizes used: {len(grid_sizes)}")
    
    # break for 2 seconds    
    time.sleep(2)
    
    # plot average num_escaped over grid sizes
    plt.plot(grid_sizes, avg_num_escaped)
    plt.xlabel('Grid Size')
    plt.ylabel('Average Number of Escaped Persons')
    plt.title('Average Number of Escaped Persons over Grid Sizes')
    plt.show()

def bottleneck_plot():
    """
    Calls to functions in simulation.py to calculate the number of bottleneck areas in the 
        simulation and then plot it.
        
        A bottleneck area is defined as any location that has more than `threshold` agents.
        
    Args:
        N/A
        
    Returns: plt - Plot of bottlneck areas over time 
    """

    # Create an empty list to store the num_people values
    simulation_list = []
    num_people_list = []  

    # This will iterate over [10, 15, 20, 25, 30]
    for num_people in range(10, 35, 5):  
        # create new instance of simulation
        simulation = Simulation(20, 20, num_people, 3, 5, [(1,1), (19,19)])
        # Store the current num_people value
        num_people_list.append(num_people) 
        # run the sim 
        run_simulation(simulation, 10)
            
    # plot
    plt.plot(simulation.escaped_counts)
    plt.xlabel('Time step')
    plt.ylabel('Number of escaped people')
    plt.title('Number of escaped people over time')
    plt.yticks(np.arange(1, max(simulation.escaped_counts) + 1 , 1))
    plt.show()

    simulation_list.append(simulation)
    print(f"Total number of people = {num_people}")
    print("End of Simulation... Moving to the next one->")
    time.sleep(2)

    simulation.plot_bottleneck_areas(simulation_list)

    # Print calculated bottleneck areas for each simulation
    for i, simulation in enumerate(simulation_list, start=1):
        # Retrieve the num_people value using the index
        num_people = num_people_list[i-1]  
        print(f"Number of bottlenecks in simulation {i} (with {num_people} people): {simulation.bottleneck_areas[-1]}")
     
    print()
    print("As time progresses in the simulation, the increase in the number of bottlenecks may suggest " + 
          "a growing complexity in the environment, potentially due to factors like agent movement, clustering, " +
          "or dynamic changes such as the spread of fires.")
    

if __name__ == "__main__":
    main()
