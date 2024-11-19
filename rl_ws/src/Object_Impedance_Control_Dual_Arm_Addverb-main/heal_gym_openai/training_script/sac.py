# '''
# # Author : Rajesh Kumar (rajesh.kumar01@addverb.com)
# # Details : This is the OpenAI SAC example for the heal robot 
# '''

# import registration
# import gymnasium as gym 

# from stable_baselines3.sac.policies import MlpPolicy
# from stable_baselines3 import PPO 


# env = gym.make("Heal-v1", render_mode="human") 

# # default device is cuda 
# model = PPO("MlpPolicy", env, verbose = 1)

# model.learn(total_timesteps=50000, log_interval=10)

# model.save("heal_cobot")

# env = model.get_env()
# obs = env.reset()

# while True:
#     action, _states = model.predict(obs)

#     obs, rewards, dones, info = env.step(action)
#     env.render("human")

import registration
import gymnasium as gym
from stable_baselines3.ppo.policies import MlpPolicy
from stable_baselines3 import PPO

env = gym.make("Heal-v1", render_mode="human") 

# Set up SAC model with modified parameters
model = PPO(
    "MlpPolicy", 
    env, 
    verbose=2)

# Train for more timesteps
model.learn(total_timesteps=5000000,log_interval=10)  # Increased timesteps

model.save("heal_spiral")

env = model.get_env()
obs = env.reset()

while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
