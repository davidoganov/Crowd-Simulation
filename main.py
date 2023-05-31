from simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np
import time

def main():
    #simulation_list = []

    # Add simulations to the list
    # grid size constant 20x20
    # Persons 10, +5 each sim
    # num fires constant 3
    # num obstacles constant 5
    # exit positions constant (1,1) (19, 19)
    simulation_list = []
    num_people_list = []  # Create an empty list to store the num_people values


    for num_people in range(10, 35, 5):  # This will iterate over [10, 15, 20, 25, 30]
        simulation = Simulation(20, 20, num_people, 3, 5, [(1,1), (19,19)])
        num_people_list.append(num_people)  # Store the current num_people value
        for step in range(10):
            simulation.step()
            simulation.agents.environment.plot(simulation.agents)
            
            
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
        num_people = num_people_list[i-1]  # Retrieve the num_people value using the index
        print(f"Number of bottlenecks in simulation {i} (with {num_people} people): {simulation.bottleneck_areas[-1]}")
     
    print()
    print("As time progresses in the simulation, the increase in the number of bottlenecks may suggest a growing complexity in the environment, potentially due to factors like agent movement, clustering, or dynamic changes such as the spread of fires.")
        

if __name__ == "__main__":
    main()
