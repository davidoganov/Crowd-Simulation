from simulation import Simulation
import matplotlib.pyplot as plt

def main():
    env_width = 20
    env_height = 20
    num_people = 10
    num_fires = 3
    num_obstacles = 5
    exit_positions = [(1,1), (0,10)]

    simulation = Simulation(env_width, env_height, num_people, num_fires, num_obstacles, exit_positions)

    for step in range(10):
        simulation.step()
        simulation.agents.environment.plot(simulation.agents)  # Plot the environment
        
    
    
    plt.plot(simulation.escaped_counts)
    plt.xlabel('Time step')
    plt.ylabel('Number of escaped people')
    plt.title('Number of escaped people over time')
    plt.show()

if __name__ == "__main__":
    main()
