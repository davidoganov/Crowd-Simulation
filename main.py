from simulation import Simulation

def main():
    env_width = 20
    env_height = 20
    num_people = 10
    num_fires = 3
    num_obstacles = 5
    exit_positions = [(10,0), (0,10)]

    simulation = Simulation(env_width, env_height, num_people, num_fires, num_obstacles, exit_positions)

    for step in range(10):
        simulation.step()
        simulation.agents.environment.plot(simulation.agents)  # Plot the environment

if __name__ == "__main__":
    main()
