import random
import time
import sys
from pacman import Directions
import game
from collections import deque
from DqnNet import *

# -p PacmanDQN -n 6000 -x 1500 -l smallGrid
# 6000 - kolvo igr

settings = {
    'epsilon': 1.0,
    'epsilon_final': 0.1,
    'epsilon_step': 10000,
    'train_iterations': 1000,  # kolvo trenirovok
    'batch_size': 32,
    'replay_mem_size': 100000,
    'discount': 0.95,
    'lr': .0002
}


def getValue(direction):
    if direction == Directions.NORTH:
        return 0.
    elif direction == Directions.EAST:
        return 1.
    elif direction == Directions.SOUTH:
        return 2.
    else:
        return 3.


def getDirection(value):
    if value == 0.:
        return Directions.NORTH
    elif value == 1.:
        return Directions.EAST
    elif value == 2.:
        return Directions.SOUTH
    else:
        return Directions.WEST


class PacmanDQN(game.Agent):
    def __init__(self, args):
        super().__init__()
        self.params = settings
        self.params['width'] = args['width']
        self.params['height'] = args['height']
        self.params['num_training'] = args['numTraining']
        self.dqn_net = DqnNet(self.params)
        self.general_record_time = time.strftime("%a %d %b %Y %H %M %S", time.localtime())
        self.Q_global = []
        self.cost_disp = 0
        self.cnt = self.dqn_net.sess.run(self.dqn_net.global_step)
        self.local_cnt = 0
        self.iteration_number = 0
        self.last_score = 0
        self.start_time = time.time()
        self.last_reward = 0.
        self.replay_memory = deque()
        self.last_scores = deque()

    def getNextMove(self):
        if np.random.rand() > self.params['epsilon']:
            self.Q_pred = self.dqn_net.sess.run(
                self.dqn_net.y,
                feed_dict={self.dqn_net.x: np.reshape(self.current_state,
                                                      (1, self.params['width'], self.params['height'], 6)),
                           self.dqn_net.q_t: np.zeros(1),
                           self.dqn_net.actions: np.zeros((1, 4)),
                           self.dqn_net.terminals: np.zeros(1),
                           self.dqn_net.rewards: np.zeros(1)})[0]

            self.Q_global.append(max(self.Q_pred))
            a_winner = np.argwhere(self.Q_pred == np.amax(self.Q_pred))

            if len(a_winner) > 1:
                move = getDirection(
                    a_winner[np.random.randint(0, len(a_winner))][0])
            else:
                move = getDirection(
                    a_winner[0][0])
        else:
            move = getDirection(np.random.randint(0, 4))
        self.last_action = getValue(move)
        return move

    def observationStep(self, state):
        if self.last_action is not None:
            self.last_state = np.copy(self.current_state)
            self.current_state = self.matricesStatesGet(state)
            self.current_score = state.getScore()
            reward = self.current_score - self.last_score
            self.last_score = self.current_score

            # Система нагороди
            if reward > 20:
                self.last_reward = 50
            elif reward > 0:
                self.last_reward = 10
            elif reward < -10:
                self.last_reward = -500
                self.won = False
            elif reward < 0:
                self.last_reward = -1

            if self.terminal and self.won:
                self.last_reward = 100.
            self.ep_rew += self.last_reward

            experience = (self.last_state, float(self.last_reward), self.last_action, self.current_state, self.terminal)
            self.replay_memory.append(experience)
            if len(self.replay_memory) > self.params['replay_mem_size']:
                self.replay_memory.popleft()

            self.modelTrain()

        self.local_cnt += 1
        self.frame += 1
        self.params['epsilon'] = max(self.params['epsilon_final'],
                                     1.00 - float(self.cnt) / float(self.params['epsilon_step']))

    def end(self, state):
        self.ep_rew += self.last_reward
        self.terminal = True
        self.observationStep(state)
        self.log()

    def observationFunction(self, state):
        self.terminal = False
        self.observationStep(state)
        return state

    def log(self):
        log_file = open('./logs/' + str(self.general_record_time) +
                        '-iteration_num-' + str(self.params['num_training']) + '.log', 'a')
        log_file.write("# %4d ; steps: %5d ; time_elapsed: %4f ; points: %12f ; epsilon: %10f " %
                       (self.iteration_number,
                        self.local_cnt,
                        time.time() - self.start_time,
                        self.ep_rew,
                        self.params['epsilon']))
        log_file.write("; Q: %10f ; won: %r \n" % (max(self.Q_global,
                                                       default=float('nan')),
                                                   self.won))
        sys.stdout.write("# %4d ; steps: %5d ; time_elapsed: %4f ; points: %12f ; epsilon: %10f " %
                         (self.iteration_number,
                          self.local_cnt,
                          time.time() - self.start_time,
                          self.ep_rew,
                          self.params['epsilon']))
        sys.stdout.write("; Q: %10f ; isWon: %r \n" % ((max(self.Q_global,
                                                            default=float('nan')),
                                                        self.won)))
        sys.stdout.flush()

    def modelTrain(self):
        if self.local_cnt > self.params['train_iterations']:
            batch = random.sample(self.replay_memory,
                                  self.params['batch_size'])

            batch_next_states = []
            batch_terminal_state = []
            batch_states = []
            batch_rewards = []
            batch_actions = []

            for i in batch:
                batch_states.append(i[0])
                batch_rewards.append(i[1])
                batch_actions.append(i[2])
                batch_next_states.append(i[3])
                batch_terminal_state.append(i[4])
            batch_states = np.array(batch_states)
            batch_rewards = np.array(batch_rewards)
            batch_next_states = np.array(batch_next_states)
            batch_terminal_state = np.array(batch_terminal_state)
            batch_actions = self.getOneHot(np.array(batch_actions))

            self.cnt, self.cost_disp = self.dqn_net.modelTrain(
                batch_states,
                batch_actions,
                batch_terminal_state,
                batch_next_states,
                batch_rewards)

    def getOneHot(self, actions):
        actions_onehot = np.zeros((self.params['batch_size'], 4))
        for i in range(len(actions)):
            actions_onehot[i][int(actions[i])] = 1
        return actions_onehot

    def matricesMerge(self, state_matrices):
        state_matrices = np.swapaxes(state_matrices, 0, 2)
        total = np.zeros((7, 7))
        for i in range(len(state_matrices)):
            total += (i + 1) * state_matrices[i] / 6
        return total

    def matricesStatesGet(self, state):

        def matrixFoodGet(game_state):
            width, height = game_state.data.layout.width, game_state.data.layout.height
            grid = game_state.data.food
            matrix = np.zeros((height, width), dtype=np.int8)
            for i in range(grid.height):
                for j in range(grid.width):
                    cell = 1 if grid[j][i] else 0
                    matrix[-1 - i][j] = cell
            return matrix

        def matrixCapsulesGet(game_state):
            width, height = game_state.data.layout.width, game_state.data.layout.height
            capsules = game_state.data.layout.capsules
            matrix = np.zeros((height, width), dtype=np.int8)
            for i in capsules:
                matrix[-1 - i[1], i[0]] = 1
            return matrix

        def matrixPacmanGet(game_state):
            width, height = game_state.data.layout.width, game_state.data.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)
            for agentState in game_state.data.agentStates:
                if agentState.isPacman:
                    pos = agentState.configuration.getPosition()
                    cell = 1
                    matrix[-1 - int(pos[1])][int(pos[0])] = cell
            return matrix

        def matrixWallGet(game_state):
            width, height = game_state.data.layout.width, game_state.data.layout.height
            grid = game_state.data.layout.walls
            matrix = np.zeros((height, width), dtype=np.int8)
            for i in range(grid.height):
                for j in range(grid.width):
                    cell = 1 if grid[j][i] else 0
                    matrix[-1 - i][j] = cell
            return matrix

        def matrixGhostGet(game_state):
            width, height = game_state.data.layout.width, game_state.data.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)
            for agentState in game_state.data.agentStates:
                if not agentState.isPacman:
                    if not agentState.scaredTimer > 0:
                        pos = agentState.configuration.getPosition()
                        cell = 1
                        matrix[-1 - int(pos[1])][int(pos[0])] = cell
            return matrix

        def matrixScaredGhostGet(game_state):
            width, height = game_state.data.layout.width, game_state.data.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)
            for agentState in game_state.data.agentStates:
                if not agentState.isPacman:
                    if agentState.scaredTimer > 0:
                        pos = agentState.configuration.getPosition()
                        cell = 1
                        matrix[-1 - int(pos[1])][int(pos[0])] = cell
            return matrix

        width, height = self.params['width'], self.params['height']
        observation = np.zeros((6, height, width))
        observation[0] = matrixWallGet(state)
        observation[1] = matrixPacmanGet(state)
        observation[2] = matrixGhostGet(state)
        observation[3] = matrixScaredGhostGet(state)
        observation[4] = matrixFoodGet(state)
        observation[5] = matrixCapsulesGet(state)
        observation = np.swapaxes(observation, 0, 2)
        return observation

    def getAction(self, state):
        move = self.getNextMove()
        legal = state.getLegalActions(0)
        if move not in legal:
            move = Directions.STOP
        return move

    def initialStateRegister(self, state):
        self.last_score = 0
        self.current_score = 0
        self.last_reward = 0.
        self.ep_rew = 0
        self.last_state = None
        self.current_state = self.matricesStatesGet(state)
        self.last_action = None
        self.terminal = None
        self.won = True
        self.Q_global = []
        self.delay = 0
        self.frame = 0
        self.iteration_number += 1
