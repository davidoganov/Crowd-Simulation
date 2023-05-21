#=============================================================================
# File: Agents
# Author(s): David Oganov
# Last Modified: 05/20/2023
#=============================================================================


"""
Class: Agents
Description: This class initializes various types of agents in the 
             crowd evacuation simulation of a public building. 
             Agents include, people, obstacles, and fire (cause of evac)
"""
class Agents():
    
    # initialize agent
    def __init__(self, xPos, yPos):
        pass
    
    """
    Class: Person
    Description: This class initializes the person agent and facilitates 
                 the movement of people in the grid environment, also tracking
                 the count of injured, alive, dead, and escaped people.
    """
    class Person():
        # initial health of person trying to escape
        health = 50
        injuredCount = 0
        escapedCount = 0
        deathCount = 0
        aliveCount = 0
        
        # init person agent
        def __init__(self, xPos, yPos):
            self.aliveCount += 1
            pass
        
        # obstacle in way or not given random position in direction of end point
        def canMove(self, xPos, yPos):
            pass
        
        # person moves in grid space, random but towards end point
        def move(self, xPos, yPos):
            pass
        
        # person agent injured from collisions 
        def injured(self, xPos, yPos):
            if self.health <= 25:
                self.injuredCount += 1
            pass
        
        def collided(self, xPos, yPos):
            self.health -= 1
            pass
        
        def die(self, xPos, yPos):
            if self.health <= 0:
                self.deathCount += 1
        
        def escaped(self, xPos, yPos):
            # check if xPos and yPos match exit point
            # if so, increment escape count
            self.escapedCount += 1
            pass
        
    """
    Class: Obstacle
    Description: This class instantiates obstacles in the public building
                 grid environment and stores each of the positions of those
                 obstacles in a list for ease of access.
    """
    class Obstacle():
        # initialize obstacle grid location
        xPosObs = 0
        yPosObs = 0
        
        # list of obstacle locations
        obsPos = []
        
        def __init__(self, xPos, yPos):
            
            pass
        
        # check if space putting new obstacle is clear 
        def clearSpace(self, xPos, yPos):
            pass
        
        # add obstacle space into list of obstacle positions
        def obstacleSpaces(self, xPos, yPos):
            pass
        
    """
    Class: Fire
    Description: This class instantiates the reason for evacuation in
                 our simulation. A fire border that moves across the grid 
                 environment as time goes on. 
    """
    class Fire():
        # 300 seconds = 5 minutes
        countDown = 300
        
        # initial positions of fire will be bottom of grid env
        def __init__(self, xPos, yPos):
            pass
        
        # checks countdown and makes call to fireSpread at time intervals
        def timer(self):
            pass
        
        # fire continues to spread 
        def fireSpread(self, xPos, yPos):
            pass
        