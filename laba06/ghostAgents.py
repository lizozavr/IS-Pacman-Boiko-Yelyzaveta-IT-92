from game import Agent, Actions
import util


# Абстрактний клас для агентів привидів
class GhostAgent(Agent):
    def __init__(self, index):
        super().__init__(index)
        self.index = index

    # Метод для отримання дії від агента
    def getAction(self, state):
        dist = self.getDistribution(state)
        return util.chooseFromDistribution(dist)

    # Повертає лічильник, що кодує розподіл над діями з наданого стану.
    def getDistribution(self, state):
        util.raiseNotDefined()


# Привид, який обирає наступну дію рівномірно випадковим чином.
class RandomGhost(GhostAgent):

    def getDistribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index): dist[a] = 1.0
        dist.normalize()
        return dist


# Привид, який вважає за краще постійно атакувати Пакмана або тікати, коли лякається.
class DirectionalGhost(GhostAgent):

    def __init__(self, index):
        super().__init__(index)
        self.index = index
        self.prob_attack = 5
        self.prob_scaredFlee = 0.8

    def getDistribution(self, state):
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared:
            speed = 0.5

        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        distancesToPacman = [util.euclideanSquaredDistance(
            pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip(
            legalActions, distancesToPacman) if distance == bestScore]

        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1 - bestProb) / len(legalActions)
        dist.normalize()
        return dist
