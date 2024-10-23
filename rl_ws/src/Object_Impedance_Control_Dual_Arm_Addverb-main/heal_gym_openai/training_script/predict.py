# move_to_state.py
import gymnasium as gym
from stable_baselines3 import PPO
import numpy as np
import registration

# Load the environment and the trained model
env = gym.make("Heal-v1", render_mode="human")
model = PPO.load("Heal")

# Define the target joint states: 1st joint to 90 degrees (pi/2), 2nd joint to -90 degrees (-pi/2)
# Remaining joints remain at zero
target_joint_states = np.array([np.pi/2, -np.pi/2, 0.0, 0.0, 0.0, 0.0])

# Reset the environment and extract the observation
obs, _ = env.reset()

# Move to the target joint states
while True:
    # Predict the action based on the observation
    action, _states = model.predict(obs)
    
    # Perform the action
    obs, reward, done, truncated, info = env.step(action)
    
    # Render the environment
    env.render()

    # Access the Mujoco data using env.unwrapped
    current_joint_states = env.unwrapped.data.qpos[:6]
    if np.linalg.norm(current_joint_states - target_joint_states) < 0.05:
        print("Reached the target joint states.")
        break

    # If the episode is done or truncated, reset the environment
    if done or truncated:
        obs, _ = env.reset()

env.close()
