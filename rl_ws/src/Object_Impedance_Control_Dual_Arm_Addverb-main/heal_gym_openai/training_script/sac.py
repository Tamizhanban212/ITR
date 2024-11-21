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

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.env_util import make_vec_env


import registration




# Create environment
# env = gym.make("Heal-v1", render_mode=None)
vec_env = make_vec_env("Heal-v1", n_envs=16)

# Create model with better hyperparameters for complex trajectory
model = PPO(
    "MlpPolicy",
    env=vec_env,
    verbose=1,
    learning_rate=1.5e-4,  # Slower learning rate for stability
    n_steps=8192,        # More steps per update
    batch_size=2048,      # Larger batch size
    n_epochs=30,         # More epochs per update
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.005,     # Less exploration
    policy_kwargs=dict(
        net_arch=dict(pi=[512, 512, 256], vf=[512, 512, 256])  # Deeper network
    ),
    tensorboard_log="./tensorboard_logs/",
    device="cuda"
)

# Add checkpointing every 50k steps
checkpoint_callback = CheckpointCallback(
    save_freq=50000,
    save_path="./logs/",
    name_prefix="infinity_model_vectorized_training"
)


# model = PPO.load("infinity_robot_vectorized_training", env=vec_env, tensorboard_log="./tensorboard_logs/")

# checkpoint_callback = CheckpointCallback(
#     save_freq=50000,
#     save_path="./logs/",
#     name_prefix="infinity_model_continued"
# )


# Train for longer (1 million steps)
print("Starting training...")
model.learn(
    total_timesteps=1_000_000,
    callback=checkpoint_callback,
    progress_bar=True,
    log_interval=5,
    reset_num_timesteps=False
)

print("Training complete! Starting evaluation...")

# Save final model
model.save("infinity_robot_vectorized_training")

# Evaluation loop
eval_env = gym.make("Heal-v1", render_mode="human")
obs, _ = eval_env.reset()

print("Press Ctrl+C to stop evaluation")
try:
    while True:
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, terminated, truncated, info = eval_env.step(action)
        
        if terminated or truncated:
            obs, _ = eval_env.reset()
        eval_env.render()
except KeyboardInterrupt:
    print("\nEvaluation stopped by user")
finally:
    eval_env.close()




















# import gymnasium as gym
# from stable_baselines3 import PPO
# from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
# from stable_baselines3.common.monitor import Monitor
# import numpy as np
# import wandb
# from wandb.integration.sb3 import WandbCallback
# import os

# import registration


# # Initialize wandb
# wandb.init(
#     project="infinity_robot",
#     name="continued_training_run",
#     config={
#         "learning_rate": 1e-4,
#         "total_timesteps": 200_000,
#         "batch_size": 256
#     }
# )


# env = Monitor(gym.make("Heal-v1", render_mode=None))
# eval_env = Monitor(gym.make("Heal-v1", render_mode=None))

# # Custom callback to track detailed metrics
# class DetailedMetricsCallback(CheckpointCallback):
#     def __init__(self, check_freq, save_path, name_prefix, verbose=1):
#         super().__init__(check_freq, save_path, name_prefix, verbose)
#         self.current_episode_rewards = []
#         self.episode_rewards = []
#         self.episode_lengths = []
    
#     def _on_step(self):
#         super()._on_step()
        
#         # Get info from current step
#         info = self.locals['infos'][0] if isinstance(self.locals['infos'], list) else self.locals['infos']
        
#         # Log to wandb
#         if 'terminal_observation' in info:  # Episode ended
#             episode_reward = sum(self.current_episode_rewards)
#             self.episode_rewards.append(episode_reward)
#             self.current_episode_rewards = []
            
#             wandb.log({
#                 "episode_reward": episode_reward,
#                 "average_reward_100": np.mean(self.episode_rewards[-100:]),
#                 "episode_length": self.locals['n_steps']
#             })
#         else:
#             self.current_episode_rewards.append(self.locals['rewards'][0])
            
#             # Log training metrics
#             if hasattr(self.model, 'logger') and len(self.model.logger.name_to_value) > 0:
#                 for key, value in self.model.logger.name_to_value.items():
#                     wandb.log({key: value})

# # Create callbacks
# metrics_callback = DetailedMetricsCallback(
#     check_freq=50000,
#     save_path="./logs/",
#     name_prefix="infinity_model_continued"
# )

# eval_callback = EvalCallback(
#     eval_env,
#     best_model_save_path="./best_model/",
#     log_path="./eval_logs/",
#     eval_freq=10000,
#     deterministic=True,
#     render=False,
#     n_eval_episodes=5
# )

# # Train with monitoring
# print("Starting training...")
# model.learn(
#     total_timesteps=1_000_000_00,
#     callback=[metrics_callback, eval_callback, WandbCallback()],
#     progress_bar=True,
#     log_interval=1,
#     reset_num_timesteps=False
# )

# print("Training complete! Starting evaluation...")
# wandb.finish()

# # Save final model
# model.save("infinity_robot_continued")

# # Evaluation loop
# eval_env = gym.make("Heal-v1", render_mode="human")
# obs, _ = eval_env.reset()

# print("Press Ctrl+C to stop evaluation")
# try:
#     while True:
#         action, _states = model.predict(obs, deterministic=True)
#         obs, rewards, terminated, truncated, info = eval_env.step(action)
#         print(f"Step reward: {rewards:.3f}")  # Print rewards during evaluation
        
#         if terminated or truncated:
#             obs, _ = eval_env.reset()
#         eval_env.render()
# except KeyboardInterrupt:
#     print("\nEvaluation stopped by user")
# finally:
#     eval_env.close()

