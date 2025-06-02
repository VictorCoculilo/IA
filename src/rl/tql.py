from timeit import default_timer as timer
import numpy as np
import pickle
from environment import Environment

class QLearningAgentTabular:

  def __init__(self, 
               env: Environment, 
               decay_rate, 
               learning_rate, 
               gamma):
    self.env = env

    self.q_table = np.zeros((env.get_num_states(), env.get_num_actions()))
    print(f"self.q_table.shape: {self.q_table.shape}")
    # self.q_table = np.zeros((env.observation_space.n, env.action_space.n))
    self.epsilon = 1.0
    self.max_epsilon = 1.0
    self.min_epsilon = 0.01
    self.decay_rate = decay_rate
    self.learning_rate = learning_rate
    self.gamma = gamma # discount rate
    self.epsilons_ = []
    
  def evaluate(self, num_episodes: int):
    total_rewards = 0

    for _ in range(num_episodes):
      terminated = False
      truncated = False

      state, _ = self.env.reset()
      state = self.env.get_state_id(state)

      while not (terminated or truncated):
        action = np.argmax(self.q_table[state])
        new_state, reward, terminated, truncated, _ = self.env.step(action)
        new_state = self.env.get_state_id(new_state)
        state = new_state
        total_rewards += reward

    return total_rewards / num_episodes

    
  def choose_action(self, state, is_in_exploration_mode=True):
    exploration_tradeoff = np.random.uniform(0, 1)

    if is_in_exploration_mode and exploration_tradeoff < self.epsilon:
      # exploration
      action = np.random.randint(self.env.get_num_actions())    
    else:
      # exploitation (taking the biggest Q value for this state)
      action = np.argmax(self.q_table[state, :])
    
    return action

  def update(self, state, action, reward, next_state):
    '''
    Apply update rule Q(s,a):= Q(s,a) + lr * [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
    '''
    self.q_table[state, action] = self.q_table[state, action] + \
      self.learning_rate * (reward + self.gamma * \
        np.max(self.q_table[next_state, :]) - self.q_table[state, action])

  def train(self, num_episodes: int):
    rewards_per_episode = []

    start_time = timer()  # Record the start time

    print()
    print('===========================================')
    print('Q-table before training:')
    print(self.q_table)

    for episode in range(num_episodes):
  
      terminated = False
      truncated = False

      state, _ = self.env.reset()
      state_id = self.env.get_state_id(state)
      state = state_id

      rewards_in_episode = []
      
      total_penalties = 0

      while not (terminated or truncated):
          
        # print(f"state: {state}")
        action = self.choose_action(state)

        # transição
        new_state, reward, terminated, truncated, info = self.env.step(action)
        new_state_id = self.env.get_state_id(new_state)
        new_state = new_state_id
        assert (not truncated)

        if reward < 0:
            total_penalties += reward

        self.update(state, action, reward, new_state)

        if (terminated or truncated):
          # Reduce epsilon to decrease the exploration over time
          self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * \
            np.exp(-self.decay_rate * episode)
          self.epsilons_.append(self.epsilon)

        state = new_state
            
        rewards_in_episode.append(reward)

      sum_rewards = np.sum(rewards_in_episode)
      rewards_per_episode.append(sum_rewards)

      if episode % 100 == 0:
        end_time = timer()  # Record the end time
        execution_time = end_time - start_time
        n_actions = len(rewards_in_episode)
        print(f"Stats for episode {episode}/{num_episodes}:") 
        print(f"\tNumber of actions: {n_actions}")
        print(f"\tTotal reward: {sum_rewards:#.2f}")
        print(f"\tExecution time: {execution_time:.2f}s")
        print(f"\tTotal penalties: {total_penalties}")
        start_time = end_time

    print()
    print('===========================================')
    print('Q-table after training:')
    print(self.q_table)

    return rewards_per_episode

  def save(self, filename):
    # open a file, where you want to store the data
    file = open(filename, 'wb')

    # dump information to that file
    pickle.dump(self, file)

    # close the file
    file.close()

  @staticmethod
  def load_agent(filename):
    # open a file, where you stored the pickled data
    file = open(filename, 'rb')

    # dump information to that file
    agent = pickle.load(file)

    return agent
