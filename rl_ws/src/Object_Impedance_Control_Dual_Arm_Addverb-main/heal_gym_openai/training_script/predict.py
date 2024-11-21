import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
import registration

# Define the new target trajectory
def generate_new_target_trajectory(start_point, end_point, num_points):
    """
    Generates a straight-line trajectory in 3D space.
    Args:
        start_point (np.ndarray): Starting position in 3D space.
        end_point (np.ndarray): Ending position in 3D space.
        num_points (int): Number of points in the trajectory.
    Returns:
        np.ndarray: Array of 3D points representing the trajectory.
    """
    return np.linspace(start_point, end_point, num_points)

# Define the start and end points for the new trajectory
start_point = np.array([-1, 0.0, 0.8])  # Adjust these based on the task/environment
end_point = np.array([1, 0.0, 0.8])
num_points = 2000
new_trajectory = generate_new_target_trajectory(start_point, end_point, num_points)

# Load the trained model
model_path = "infinity_robot_vectorized_training"
model = PPO.load(model_path)

# Load the real environment
env = gym.make("Heal-v1", render_mode="human")

# Reset the environment and extract the initial observation
obs, _ = env.reset()

# Move along the new trajectory
target_reached = False
total_rewards = 0
steps = 0

print("Evaluating the model on the new target trajectory...")
try:
    for target_point in new_trajectory:
        while True:
            # Predict the action based on the observation
            action, _ = model.predict(obs, deterministic=True)

            # Perform the action
            obs, reward, terminated, truncated, info = env.step(action)

            # Render the environment
            env.render()

            # Access the end-effector position
            current_end_effector_position = env.unwrapped.data.body("end_effector").xpos[:3]

            # Compute the distance to the target point
            distance_to_target = np.linalg.norm(current_end_effector_position - target_point)

            # Update metrics
            total_rewards += reward
            steps += 1

            # Check if the end-effector has reached the current target point
            if distance_to_target < 0.05:
                print(f"Reached target point: {target_point}, Current Position: {current_end_effector_position}")
                break

            # If the episode ends, reset the environment
            if terminated or truncated:
                print(f"Episode terminated early. Total rewards: {total_rewards}, Steps: {steps}")
                obs, _ = env.reset()
                total_rewards = 0
                steps = 0

except KeyboardInterrupt:
    print("\nEvaluation interrupted by user.")

# Close the environment
env.close()




# import gymnasium as gym
# from stable_baselines3 import PPO
# import numpy as np
# import registration

# # Load the environment and the trained model
# env = gym.make("Heal-v1", render_mode="human")
# model = PPO.load("heal_spiral")

# # Define the initial joint states
# initial_joint_states = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# # Define a target trajectory to move 10 cm to the -x, 10 cm to the +x, and back to the initial point
# num_timesteps = 1000

# # Generate the target trajectory
# target_trajectory = [
#     initial_joint_states + np.array([0.0, 0.5 * (i / num_timesteps), 0.0, 0.0, 0.0, 0.0]) for i in range(num_timesteps)
# ]

# # Reset the environment and extract the observation
# obs, _ = env.reset()

# # Move to the target trajectory
# for target_joint_states in target_trajectory:
#     while True:
#         # Predict the action based on the observation
#         action, _states = model.predict(obs)

#         # Perform the action
#         obs, reward, done, truncated, info = env.step(action)

#         # Render the environment
#         env.render()

#         # Access the Mujoco data using env.unwrapped
#         current_joint_states = env.unwrapped.data.qpos[:6]
#         print(current_joint_states)
#         if np.linalg.norm(current_joint_states - target_joint_states) < 0.005:
#             print("Reached the target joint states.")
#             break

#         # # If the episode is done or truncated, reset the environment
#         # if done or truncated:
#         #     obs, _ = env.reset()

# env.close()
