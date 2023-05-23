#=============================================================================
# File: Agents
# Author(s): David Oganov
# Last Modified: 05/22/2023
#=============================================================================
import numpy as np
from Environment import Environment

# For time being, this file assumes the grid size to be 100 x 100

class Agents():
    """
    Class: Agents
    Description: This class initializes various types of agents in the 
                 crowd evacuation simulation of a public building. 
                 Agents include, people, obstacles, and fire (cause of evac)
    Attributes: Env - the environment currently being used. 
        
    Methods:
        __init__(self, xPos: int, yPos: int): Initializes Agents
    """
    
    def __init__(self, xPos: int, yPos: int):
        """
        Initializes agents: 
            sets people at start border (bottom row of grid)
            sets fire at west column 
            sets obstacles in-between start border and fire (mock doorways)
            sets exit point at top right corner of the grid
        
        Args:
            xPos (int): The x-coordinate of the position.
            yPos (int): The y-coordinate of the position.
        
        Returns: N/A
        """
        # set people at start border
        for x in range(Environment.grid.shape[0]):
            Environment.grid[x, 0] = Agents.Person(x, 0)
        
        # set fire at west column
        for y in range(Environment.grid.shape[1]):
            Environment.grid[0, y] = Agents.Fire(0, y)
        
        # set obstacles in-between start border and fire
        for x in range(1, xPos):
            for y in range(1, yPos):
                Environment.grid[x, y] = Agents.Obstacle(x, y)
        
        # set exit point at top right corner of the grid
        Environment.grid[xPos, yPos] = Agents.Exit()
    
    class Person():
        """
        Class: Person
        Description: This class initializes the person agent and facilitates 
                     the movement of people in the grid environment, also tracking
                     the count of injured, alive, dead, and escaped people.
        Attributes: health - person agents health reaches 25 = injured, 0 = dead
                    injuredCount - # of people injured (cannot move)
                    escapedCount - # of people escaped (reached exit)
                    deathCount - # of people killed (health == 0)
                    aliveCount - # of living persons 
                    persons: List of persons currently in the environment
        Methods: __init__: Initializes a person agent, keeping count & establishing health
                canMove: Boolean helper to determine if space person trying to enter is valid
                move: Moves the person agent to another point in the grid 
                isInjured: Boolean that returns true if health <= 25, increment count
                collided: Boolean that returns true if person collides with another person agent
                isDead: Boolean to return whether person agent heatlh == 0, if true increments deathCount
                escaped: Boolean that returns true if person agent has reached exit point
        """

        health = 50
        injuredCount = 0
        escapedCount = 0
        deathCount = 0
        aliveCount = 0
        persons = []
        
        def __init__(self, xPos: int, yPos: int):
            """
            Initializes a person agent, keeping count & establishing health
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                n/a 
            """
            self.__class__.aliveCount += 1
            self.xPos = xPos
            self.yPos = yPos
            
        
        def canMove(self, xPos: int, yPos: int) -> bool:
            """
            Boolean helper to determine if space person trying to enter is valid
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                Bool - True: Can move to given space False: Cannot move to space 
            """
            # check within bounds
            if (Environment.is_within_bounds(self, xPos, yPos) == False):
                return False
            
            # check if the space is not an obstacle
            if Environment.grid[xPos, yPos] == Agents.Obstacle.barrier:
                return False
            
            # check if the space is not occupied by another person
            for person in Agents.Person.persons:
                if (person.xPos == xPos) and (person.yPos == yPos) and (person != self):
                    return False
        
            return True
        
        def move(self, xPos: int, yPos: int):
            """
            Moves the person agent to another point in the grid 
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: N/A
            """
            if self.canMove(xPos, yPos):
                self.xPos = xPos
                self.yPos = yPos
        
        def isInjured(self, xPos: int, yPos: int) -> bool:
            """
            Boolean that returns true if health <= 25, increment count
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: 
                True if health <= 25 else False
            """
            if self.health <= 25:
                self.injuredCount += 1
                return True
            else:
                return False
        
        def collided(self, xPos: int, yPos: int):
            """
            Boolean that returns true if Person agent collides with another Person agent
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                Bool - true if Person agent in same space (collision) with another Person agent
            """
            for person in self.persons:
                if (person != self) and (person.xPos == xPos) and (person.yPos == yPos):
                    self.health -= 1  # reduce health by 1
                    return True  # collision occurred with another person agent
            return False  # no collision occurred
            
        def isDead(self, xPos: int, yPos: int) -> bool:
            """
           Boolean to return whether person agent heatlh == 0, if true increments deathCount
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                Bool - True: Person agent heatlh == 0 False: Person agent health > 0
            """
            if self.health <= 0:
                self.deathCount += 1
        
        def escaped(self, xPos: int, yPos: int):
            """
            Boolean that returns true if person agent has reached exit point
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                Bool - True: Person agent at exit point False: Not escaped 
            """
            if (self.Exit.reached(xPos, yPos)): # check position against exit
                self.escapedCount += 1 # raise escapedCount
                return True
            else:
                return False
            

    class Obstacle():
        """
        Class: Obstacle
        Description: This class instantiates obstacles in the public building
                     grid environment and stores each of the positions of those
                     obstacles in a list for ease of access.
        Attributes: xPosObs - the x-coordinate of the position of the obstacle
                    yPosObs - the y-coordinate of the position of the obstacle
                    obsPos - numpy array of obstacle positions in environment
                    maxObs - The maximum number of obstacles in the environment
        Methods: __init__: Initializes obstacles, keeping track of obs positions
                 clearSpace: Boolean to see if obstacle already placed in position
                 obstacleSpaces: Adds current position obstacle into array of obstacle positions
        """
        # initialize obstacle grid location
        xPosObs = 0
        yPosObs = 0
        maxObs = 15
        
        # empty array 15x15 of tuples
        obsPos = np.empty((15, 15), dtype=object)
        
        def __init__(self, xPos: int, yPos: int):
            """
            Initializes obstacles, keeping track of obstacle positions
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: N/A
            """
            self.xPosObs = xPos
            self.yPosObs = yPos
            self.obstacleSpaces(xPos, yPos)
        
        def clearSpace(self, xPos: int, yPos: int) -> bool:
            """
            Boolean to see if obstacle already placed in position
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                Bool - True: Empty Space False: Obstacle already in space
            """
            if self.obsPos[xPos][yPos] is None:
                 return True
            else:
                 return False
        
        def obstacleSpaces(self, xPos: int, yPos: int):
            """
            Adds current position obstacle into list of obstacle positions
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: N/A
            """
            for i in range(self.maxObs):
                for j in range(self.maxObs):
                    if self.obsPos[i, j] is None: # assign position 
                        self.obsPos[i, j] = (xPos, yPos)
                        break
                    else:
                        continue
                    break
        
        
    class Fire():
        """
        Class: Fire
        Description: This class instantiates the reason for evacuation in
                     our simulation. A fire border that moves across the grid 
                     environment as time goes on. 
        Attributes: countDown: Sets time to manage simulation time & fire progression
                    damage: Damage done when in contact with Person agent
                    barrier: Indicator of no move position for Person agents
        Methods: __init__: Sets the initial fire position along south side of grid
                timer: Performs a decrement of the timer, progressing the fire as it goes
                fireSpread: Moves the fire as countdown goes on
                calculateEffect: Checks and applies damage to any Person agents
        """
        # 300 seconds = 5 minutes
        countDown = 300
        damage = 10
        barrier = -1
        # add fire intensity level which influences spaces moved by person agent at one move ??
        
        def __init__(self, xPos: int, yPos: int):
            """
            Sets the initial fire position along south side of grid
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: N/A
            """
            self.xPos = xPos
            self.yPos = yPos
            
        
        def timer(self):
            """
            Performs a decrement of the timer, progressing the fire as it goes
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                int - value of the countDown variable
            """
            self.countDown -= 1
            return self.countDown

        def fireSpread(self, xPos: int, yPos: int):
            """
            Moves the fire as countdown goes on
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: N/A
            """
            self.xPos = xPos + 1
        
        def calculateEffect(self, xPos: int, yPos: int):
            """
            Checks and applies damage to any Person agents
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: N/A
            """
            for person in self.persons:
                if (person.xPos == xPos) and (person.yPos == yPos):
                    person.health -= self.damage
                
                
    class Exit():
        """
        Class: Exit
        Description: This class instantiates the 'exit door', person
                     agents are attracted to this agent and will move
                     towards it. Reaching this agent space will equal
                     evacuating the building successfully.
        Attributes: freedom - Attractiveness variable to entice Person agents towards it
        Methods: __init__: Initializes the exit door in the top right corner of the grid
                 reached: Boolean notes Person agent as reached the exit successfully, updating counters
                          as needed. 
                 fireReached: Boolean returning true if the fire has reached the exit door, ending
                              the Person agents ability to escape, completing simulation
        """
        freedom = 100
        # assumed right now that grid will be ~ 100x100
        exitX = 100
        exitY = 0
        
        def __init__(self, xPos = exitX, yPos = exitY):
            """
            Initializes the exit door in the top right corner of the grid
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns: N/A
            """
            self.freedom = Environment.grid[xPos, yPos]
    
        
        def reached(self, xPos: int, yPos: int) -> bool:
            """
            Boolean notes Person agent as reached the exit successfully, 
                updating counters as needed. 
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                Bool - True: Person agent reached exit successfully else False 
            """
            if (xPos == self.exitX) and (yPos == self.exitY):
                self.escapedCount += 1
                return True
            else:
                return False
        
        def fireReached(self, xPos: int, yPos: int) -> bool:
            """
            Boolean returning true if the fire has reached the exit door, ending
                the Person agents ability to escape, completing simulation
            
            Args:
                xPos (int): The x-coordinate of the position.
                yPos (int): The y-coordinate of the position.
            
            Returns:
                Bool - True: Fire reached exit door else False 
            """
            if (xPos == self.exitX) and (yPos == self.exitY):
                # Check if the fire has reached the exit door
                if self.Environment.grid[xPos, yPos] == self.Fire.barrier:  # Fire.barrier represents the fire
                    return True
                return False
        