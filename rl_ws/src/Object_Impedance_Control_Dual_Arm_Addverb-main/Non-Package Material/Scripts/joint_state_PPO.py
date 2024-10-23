import gymnasium as gym
from stable_baselines3 import PPO
import numpy as np

# Ensure the path to your environment is included
import sys
sys.path.append('/home/tamizhanban/Documents/ITR/rl_ws/src/Object_Impedance_Control_Dual_Arm_Addverb-main/heal_gym_openai')

# Import custom environment
from env.heal_env import HealEnv

# Register custom environment
gym.envs.registration.register(
    id='Heal-v1',
    entry_point='env.heal_env:HealEnv',
    max_episode_steps=500,
)

# Define target joint state
target_joint_state = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

# Create environment
env = gym.make('Heal-v1')

# Load the model
model = PPO.load("Heal")

# Function to move to target joint state
def move_to_joint_state(env, model, target_state, max_steps=500):
    obs = env.reset()
    for step in range(max_steps):
        action, _states = model.predict(obs)
        env.step(action)
        env.render()
        
        # Get current joint state
        current_state = env._get_obs()[:6]
        
        # Check if target state is reached
        if np.allclose(current_state, target_state, atol=0.01):
            print(f"Target joint state reached in {step} steps.")
            break
    else:
        print("Failed to reach target joint state within max steps.")

# Move the Heal robot to the target joint state
move_to_joint_state(env, model, target_joint_state)
