import numpy as np
import os
from gymnasium import utils
from gymnasium.spaces import Box
from gymnasium.envs.mujoco import MujocoEnv
from configparser import ConfigParser

class HealEnv(MujocoEnv):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps": 100,
    }

    def __init__(self, render_mode="human"):
        self.render_mode = render_mode
        configur = ConfigParser()
        path = os.path.dirname(os.path.abspath(__file__))
        configur.read(os.path.join(path, "config.ini"))

        self.frame_skip = configur.getint('Default', 'skip_frame')
        self.episode_len = configur.getint('Default', 'episode_len')

        # Initialize MuJoCo environment
        MujocoEnv.__init__(self, os.path.abspath(os.path.join(path, configur.get('Default', 'path'))),
                           self.frame_skip, observation_space=None, render_mode=render_mode)

        # Disable gravity
        self.model.opt.gravity[:] = 0  # Set gravity to zero

        # Set up observation and action spaces
        obs_dim = self.model.nq + self.model.nv + self.model.nv
        self.observation_space = Box(
            low=-np.inf,
            high=np.inf,
            shape=(obs_dim,),
            dtype=np.float64
        )

        min_action = configur.getfloat('Default', 'min_action')
        max_action = configur.getfloat('Default', 'max_action')
        bounds = self.model.actuator_ctrlrange.copy().astype(np.float64)
        low, high = bounds.T
        low.fill(min_action)
        high.fill(max_action)
        self.action_space = Box(low=low, high=high, dtype=np.float64)

        # Initialize state variables
        self.step_number = 0
        self.initial_ee_height = None
        self.initial_joint_positions = None

        # Initialize with proper dimensions
        self.init_pos = np.zeros(self.model.nq)
        self.init_vel = np.zeros(self.model.nv)

        # Do initial simulation step
        self.do_simulation(np.zeros(self.model.nu), self.frame_skip)

        # Store initial positions as targets
        self.initial_ee_height = self.data.body("end_effector").xpos[2]
        self.initial_joint_positions = self.data.qpos.copy()

        # Define parameters for the circular path
        self.path_radius = 0.8  # Define the radius of the circle
        self.num_points = 2000  # Number of points along the path

        # Generate the circular trajectory path
        self.path = self.generate_circular_path(self.path_radius, self.num_points)

        self.num_points = len(self.path)  # Update number of points to be the length of the path
        self.current_target_idx = 0

    def generate_circular_path(self, radius, num_points):
        """Generates a circular path in the XY plane with a constant height."""
        t_values = np.linspace(0, 2 * np.pi, num_points)
        path = np.array([
            [radius * np.cos(t), radius * np.sin(t), self.initial_ee_height]  # Z-coordinate stays constant
            for t in t_values
        ])
        return path

    def _get_obs(self):
        """Returns the current state of the system, including joint positions and velocities."""
        obs = np.concatenate([self.data.qpos, self.data.qvel, self.data.qacc])
        return obs

    def reset_model(self):
        self.step_number = 0
        self.current_target_idx = 0

        # Reset to initial position with small random noise
        noise_scale = 0.01
        self.init_pos = self.initial_joint_positions + np.random.uniform(
            -noise_scale,
            noise_scale,
            size=self.model.nq
        )
        self.init_vel = np.zeros(self.model.nv)

        self.set_state(self.init_pos, self.init_vel)
        return self._get_obs()

    def get_reward(self):
        ee_pos = self.data.body("end_effector").xpos
        current_target = self.path[self.current_target_idx]

        # 1. Path Following Reward
        distance_to_path = np.linalg.norm(ee_pos - current_target)
        path_reward = -8.0 * distance_to_path  # Base penalty for distance from target

        # 2. Smooth Motion Reward
        ee_velocity = self.data.body("end_effector").cvel[3:6]  # Linear velocity of end effector
        velocity_magnitude = np.linalg.norm(ee_velocity)
        desired_velocity = 5.0  # Desired constant velocity magnitude
        velocity_reward = -3.0 * abs(velocity_magnitude - desired_velocity)

        # 3. Progress Reward
        if distance_to_path < 0.03:  # Threshold for considering a point reached
            progress_reward = 30.0
        else:
            progress_reward = 0.0

        # Combine all rewards
        total_reward = path_reward + velocity_reward + progress_reward
        return total_reward

    def step(self, action):
        """Apply position control by setting joint positions (action)."""
        self.data.ctrl[:] = action
        self.do_simulation(action, self.frame_skip)
        self.step_number += 1

        obs = self._get_obs()
        reward = self.get_reward()
        done = False  # Always false to ensure the loop continues
        truncated = self._is_truncated()

        # Update target if the end effector is close to the current path target
        if np.linalg.norm(self.data.body("end_effector").xpos - self.path[self.current_target_idx]) < 0.05:
            # Move to the next point on the path, wrapping back to the start if at the end
            self.current_target_idx = (self.current_target_idx + 1) % self.num_points

        # Update visualization (if enabled)
        if self.render_mode == "human":
            self.render()

        return obs, reward, done, truncated, self._get_info()

    def is_done(self):
        """Override this function to prevent termination based on height."""
        return False  # Prevent the episode from terminating early

    def _is_truncated(self):
        return self.step_number >= self.episode_len

    def _get_info(self):
        return {
            'end_effector_height': self.data.body("end_effector").xpos[2],
            'initial_height': self.initial_ee_height,
            'joint_velocities': self.data.qvel.copy(),
            'current_target_idx': self.current_target_idx,
            'distance_to_target': np.linalg.norm(self.data.body("end_effector").xpos - self.path[self.current_target_idx])
        }


# import numpy as np
# import os
# from gymnasium import utils
# from gymnasium.spaces import Box
# from gymnasium.envs.mujoco import MujocoEnv
# from configparser import ConfigParser

# class HealEnv(MujocoEnv):
#     metadata = {
#         "render_modes": [
#             "human",
#             "rgb_array",
#             "depth_array",
#         ],
#         "render_fps": 100,
#     }

#     def __init__(self, render_mode="human"):
#         self.render_mode = render_mode
#         configur = ConfigParser()
#         path = os.path.dirname(os.path.abspath(__file__))
#         configur.read(os.path.join(path, "config.ini"))

#         self.frame_skip = configur.getint('Default', 'skip_frame')
#         self.episode_len = configur.getint('Default', 'episode_len')

#         # Initialize MuJoCo environment
#         MujocoEnv.__init__(self, os.path.abspath(os.path.join(path, configur.get('Default', 'path'))),
#                            self.frame_skip, observation_space=None, render_mode=render_mode)

#         # Disable gravity
#         self.model.opt.gravity[:] = 0  # Set gravity to zero

#         # Set up observation and action spaces
#         obs_dim = self.model.nq + self.model.nv + self.model.nv
#         self.observation_space = Box(
#             low=-np.inf,
#             high=np.inf,
#             shape=(obs_dim,),
#             dtype=np.float64
#         )

#         min_action = configur.getfloat('Default', 'min_action')
#         max_action = configur.getfloat('Default', 'max_action')
#         bounds = self.model.actuator_ctrlrange.copy().astype(np.float64)
#         low, high = bounds.T
#         low.fill(min_action)
#         high.fill(max_action)
#         self.action_space = Box(low=low, high=high, dtype=np.float64)

#         # Initialize state variables
#         self.step_number = 0
#         self.initial_ee_height = None
#         self.initial_joint_positions = None

#         # Initialize with proper dimensions
#         self.init_pos = np.zeros(self.model.nq)
#         self.init_vel = np.zeros(self.model.nv)

#         # Do initial simulation step
#         self.do_simulation(np.zeros(self.model.nu), self.frame_skip)

#         # Store initial positions as targets
#         self.initial_ee_height = self.data.body("end_effector").xpos[2]
#         self.initial_joint_positions = self.data.qpos.copy()

#         # Generate the triangular trajectory path
#         self.path = self.generate_triangle_path(0.01)

#         self.num_points = len(self.path)  # Update number of points to be the length of the path
#         self.current_target_idx = 0

#     def generate_triangle_path(self, side_length):
#         """Generates a small equilateral triangle path in the XY plane with a constant height."""
#         start_x = self.data.body("end_effector").xpos[0]
#         start_y = self.data.body("end_effector").xpos[1]
#         z = self.initial_ee_height

#         # Equilateral triangle vertices
#         A = np.array([start_x, start_y, z])
#         B = np.array([start_x + side_length, start_y, z])
#         C = np.array([start_x + 0.5 * side_length, start_y + np.sin(np.deg2rad(60)) * side_length, z])

#         # Points on the path (triangle perimeter)
#         path = np.linspace(A, B, self.episode_len//3).tolist()
#         path += np.linspace(B, C, self.episode_len//3).tolist()
#         path += np.linspace(C, A, self.episode_len//3).tolist()

#         return np.array(path)

#     def _get_obs(self):
#         """Returns the current state of the system, including joint positions and velocities."""
#         obs = np.concatenate([self.data.qpos, self.data.qvel, self.data.qacc])
#         return obs

#     def reset_model(self):
#         self.step_number = 0
#         self.current_target_idx = 0

#         # Reset to initial position with small random noise
#         noise_scale = 0.01
#         self.init_pos = self.initial_joint_positions + np.random.uniform(
#             -noise_scale,
#             noise_scale,
#             size=self.model.nq
#         )
#         self.init_vel = np.zeros(self.model.nv)

#         self.set_state(self.init_pos, self.init_vel)
#         return self._get_obs()

#     def get_reward(self):
#         ee_pos = self.data.body("end_effector").xpos
#         current_target = self.path[self.current_target_idx]

#         # 1. Path Following Reward
#         distance_to_path = np.linalg.norm(ee_pos - current_target)
#         path_reward = -10.0 * distance_to_path  # Base penalty for distance from target

#         # 2. Smooth Motion Reward
#         ee_velocity = self.data.body("end_effector").cvel[3:6]  # Linear velocity of end effector
#         velocity_magnitude = np.linalg.norm(ee_velocity)
#         desired_velocity = 8.0  # Desired constant velocity magnitude
#         velocity_reward = -5.0 * abs(velocity_magnitude - desired_velocity)

#         # 3. Progress Reward
#         if distance_to_path < 0.05:  # Threshold for considering a point reached
#             progress_reward = 50.0
#         else:
#             progress_reward = 0.0

#         # Combine all rewards
#         total_reward = path_reward + velocity_reward + progress_reward
#         return total_reward

#     def step(self, action):
#         """Apply position control by setting joint positions (action)."""
#         self.data.ctrl[:] = action
#         self.do_simulation(action, self.frame_skip)
#         self.step_number += 1

#         obs = self._get_obs()
#         reward = self.get_reward()
#         done = False  # Always false to ensure the loop continues
#         truncated = self._is_truncated()

#         # Update target if the end effector is close to the current path target
#         if np.linalg.norm(self.data.body("end_effector").xpos - self.path[self.current_target_idx]) < 0.05:
#             # Move to the next point on the path, wrapping back to the start if at the end
#             self.current_target_idx = (self.current_target_idx + 1) % self.num_points

#         # Update visualization (if enabled)
#         if self.render_mode == "human":
#             self.render()

#         return obs, reward, done, truncated, self._get_info()

#     def is_done(self):
#         """Override this function to prevent termination based on height."""
#         return False  # Prevent the episode from terminating early

#     def _is_truncated(self):
#         return self.step_number >= self.episode_len

#     def _get_info(self):
#         return {
#             'end_effector_height': self.data.body("end_effector").xpos[2],
#             'initial_height': self.initial_ee_height,
#             'joint_velocities': self.data.qvel.copy(),
#             'current_target_idx': self.current_target_idx,
#             'distance_to_target': np.linalg.norm(self.data.body("end_effector").xpos - self.path[self.current_target_idx])
#         }
