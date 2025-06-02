import gym
from blackjack_environment import BlackjackEnvironment
from tql import QLearningAgentTabular

# Cria o ambiente do Gym
base_env = gym.make('Blackjack-v1')

# Adapta para seu ambiente customizado com mapeamento
env = BlackjackEnvironment(base_env)

# Cria o agente Q-learning
agent = QLearningAgentTabular(
    env=env,
    decay_rate=0.005,
    learning_rate=0.1,
    gamma=0.99
)

# Treina o agente
reward_history = agent.train(num_episodes=10000)

# Avalia desempenho
avg_reward = agent.evaluate(num_episodes=1000)
print(f"Recompensa média após treino: {avg_reward:.2f}")
