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
# model.learn(total_timesteps=100000)
# model.save("Heal")


# model = PPO.load("Heal")

# obs = vec_env.reset()
# while True:
#     action, _states = model.predict(obs)
#     print(action)
#     obs, rewards, dones, info = vec_env.step(action)
#     vec_env.render("human")

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import registration
from stable_baselines3.common.callbacks import BaseCallback

# Early Stopping Callback
class EarlyStoppingCallback(BaseCallback):
    def __init__(self, check_freq: int, threshold: float, verbose=0):
        super(EarlyStoppingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.threshold = threshold

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            infos = self.locals['infos']
            for info in infos:
                if 'loss' in info and info['loss'] < self.threshold:
                    if self.verbose > 0:
                        print(f"Stopping training early! Loss has reached below {self.threshold}")
                    return False
        return True

# Parallel environments
vec_env = make_vec_env("Heal-v1", n_envs=4)
model = PPO("MlpPolicy", vec_env, verbose=1, device="cuda")

# Instantiate the callback
early_stopping_callback = EarlyStoppingCallback(check_freq=10000, threshold=0.1, verbose=1)

# Train the model with the callback
model.learn(total_timesteps=50000, callback=early_stopping_callback)
model.save("Heal")

model = PPO.load("Heal")
obs = vec_env.reset()

while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    print(obs)
    vec_env.render("human")

