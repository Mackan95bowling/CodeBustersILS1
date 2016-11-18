"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def graphSearch(problem, fringe):
    closed = []
    fringe.push(Node(problem.getStartState()))
    while True:
        if fringe.isEmpty():
            return None
        node = fringe.pop()
        if problem.isGoalState(node.state):
            path = []
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return path
        if node.state not in closed:
            closed.append(node.state)

            expands = expand(node, problem)
            for i in expands:
               fringe.push(i)





def expand(node, problem):
    successors = []
    succ = problem.getSuccessors(node.state)
    for t in succ:
        s = Node()
        s.parent = node
        s.action = t[1]
        s.state = t[0]
        s.cost = node.cost + t[2]
        s.depth = node.depth + 1
        successors.append(s)
    return successors

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    fringe = util.Stack() correct?
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    return graphSearch(problem, fringe)

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first.
        fringe = util.Queue() priority can be used 2 ,correct?
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    return graphSearch(problem, fringe)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first.
        fringe = util.PriorityQueue() correct?
    """
    "*** YOUR CODE HERE ***"

    def priorityFunction(node):

      # strategy open the cheapest node... cheapest = lowest node.cost
        return node.cost

    fringe = util.PriorityQueueWithFunction(priorityFunction)
    return graphSearch(problem, fringe)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def aStarPriority(node):

     return node.cost + heuristic(node.state,problem)
    fringe = util.PriorityQueueWithFunction(aStarPriority)
    return graphSearch(problem, fringe)
    util.raiseNotDefined()

class Node:

    def __init__(self, state = None, parent = None, action = None, depth = 0, cost = 0):
        self.parent = parent
        self.state = state
        self.action = action
        self.depth = depth
        self.cost = cost



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
