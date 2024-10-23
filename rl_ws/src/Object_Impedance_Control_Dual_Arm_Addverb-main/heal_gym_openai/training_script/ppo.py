# '''
#     # Author : Rajesh Kumar (rajesh.kumar01@addverb.com)
#     # Details : This is the OpenAI PPO example for the heal robot with multiple vectorized environments 
# '''

# import gymnasium as gym 

# from stable_baselines3 import PPO
# from stable_baselines3.common.env_util import make_vec_env
# import registration

# # Parallel environments
# # N envs = no of environments to be created 
# vec_env = make_vec_env("Heal-v1", n_envs=4)

# model = PPO("MlpPolicy", vec_env, verbose=1, device="cuda")
# model.learn(total_timesteps=25000)
# model.save("Heal")


# model = PPO.load("Heal")

# obs = vec_env.reset()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = vec_env.step(action)
#     vec_env.render("human")

# ppo.py
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import registration

# Create multiple parallel environments
vec_env = make_vec_env("Heal-v1", n_envs=4)

# Initialize the PPO model
model = PPO(
    "MlpPolicy",
    vec_env,
    learning_rate=1e-4,  # Lower learning rate
    n_steps=2000,  # Increase the number of steps per update
    batch_size=100,
    clip_range=0.01,  # Reduce the clipping range
    verbose=1,
    device="cuda"
)


# Train the model
model.learn(total_timesteps=50000)
model.save("Heal")

# Test the trained model
obs = vec_env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render("human")
