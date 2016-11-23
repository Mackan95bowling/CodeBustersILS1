from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide. You are welcome to change
      it in any way you see fit, so long as you don't touch the method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPosition = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        ghostDistance = [util.manhattanDistance(newPos, ghost) for ghost in newGhostPosition]
        foodDistance = [util.manhattanDistance(newPos, food) for food in newFood.asList()]

        if currentGameState.getPacmanPosition() == newPos:
            return -10000

        for ghostD in ghostDistance:
            if ghostD < 2:
                return -10000

        if foodDistance == 0:
            return 1000000

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents. Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended. Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        numAgent = gameState.getNumAgents()
        legalaction = gameState.getLegalActions(0)
        maximum = -1000
        depth = 0
        for action in legalaction:
            state = gameState.generateSuccessor(0, action)
            val = self.value(state, 1, depth, numAgent)

            if val > maximum:
                maximum = val
                maxAction = action
        print "print", maximum
        return maxAction

    def value(self, gameState, agent, depth, numAgent):
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent == 0:
            depth = depth + 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            return self.Maxvalue(gameState, agent, depth, numAgent)
        return self.Minvalue(gameState, agent, depth, numAgent)

    def Maxvalue(self, gameState, agent, depth, numAgent):
        max = -9999
        agentNext = (agent + 1) % numAgent
        action = gameState.getLegalActions(agent)
        for actions in action:
            state = gameState.generateSuccessor(agent, actions)
            val = self.value(state, agentNext, depth, numAgent)
            if val > max:
              max = val
        return max

    def Minvalue(self, gameState, agent, depth, numAgent):
        min = 9999
        agentNext = (agent + 1) % numAgent
        action = gameState.getLegalActions(agent)
        for actions in action:
            state = gameState.generateSuccessor(agent, actions)
            val = self.value(state, agentNext, depth, numAgent)
            if val < min:
                min = val
        return min

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        A = 0
        B = 0
        numAgent = gameState.getNumAgents()
        legalaction = gameState.getLegalActions(0)
        maximum = -1000
        depth = 0
        for action in legalaction:
            state = gameState.generateSuccessor(0, action)
            val = self.value(state, 1, depth, numAgent,A,B)

            if val > maximum:
                maximum = val
                maxAction = action
        print "print", maximum
        return maxAction

    def value(self, gameState, agent, depth, numAgent,A,B):
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent == 0:
            depth = depth + 1
            if depth == self.depth:
                return self.evaluationFunction(gameState)
            return self.Maxvalue(gameState, agent, depth, numAgent,A,B)
        return self.Minvalue(gameState, agent, depth, numAgent,A,B)

    def Maxvalue(self, gameState, agent, depth, numAgent, A, B):
        maxi = -9999
        agentNext = (agent + 1) % numAgent
        action = gameState.getLegalActions(agent)
        for actions in action:
            state = gameState.generateSuccessor(agent, actions)
            val = self.value(state, agentNext, depth, numAgent,A,B)
            if val > maxi:
                maxi = val
            if maxi >= B:
                return maxi
            A = max(A, maxi)
        return maxi

    def Minvalue(self, gameState, agent, depth, numAgent,A,B):
        mini = 9999
        agentNext = (agent + 1) % numAgent
        action = gameState.getLegalActions(agent)
        for actions in action:
            state = gameState.generateSuccessor(agent, actions)
            val = self.value(state, agentNext, depth, numAgent,A,B)
            if val < mini:
                mini = val
            if mini <= A:
                return mini
            B = min(B,mini)
        return mini

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

