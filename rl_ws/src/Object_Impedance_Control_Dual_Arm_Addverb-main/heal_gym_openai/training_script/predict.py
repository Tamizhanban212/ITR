import gymnasium as gym
from stable_baselines3 import PPO
import numpy as np
import registration

# Load the environment and the trained model
env = gym.make("Heal-v1", render_mode="human")
model = PPO.load("heal_spiral")

# Define the initial joint states
initial_joint_states = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# Define a target trajectory to move 10 cm to the -x, 10 cm to the +x, and back to the initial point
num_timesteps = 100

# Generate the target trajectory
target_trajectory = [
    initial_joint_states + np.array([0.0, 0.57 * (i / num_timesteps), 0.0, 0.0, 0.0, 0.0]) for i in range(num_timesteps)
]

# Reset the environment and extract the observation
obs, _ = env.reset()

# Move to the target trajectory
for target_joint_states in target_trajectory:
    while True:
        # Predict the action based on the observation
        action, _states = model.predict(obs)

        # Perform the action
        obs, reward, done, truncated, info = env.step(action)

        # Render the environment
        env.render()

        # Access the Mujoco data using env.unwrapped
        current_joint_states = env.unwrapped.data.qpos[:6]
        print(current_joint_states)
        if np.linalg.norm(current_joint_states - target_joint_states) < 0.05:
            print("Reached the target joint states.")
            break

        # If the episode is done or truncated, reset the environment
        if done or truncated:
            obs, _ = env.reset()

env.close()
