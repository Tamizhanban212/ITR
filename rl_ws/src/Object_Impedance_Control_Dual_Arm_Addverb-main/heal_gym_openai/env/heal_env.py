# # Author : Rajesh Kumar (rajesh.kumar01@addverb.com)
# # Details : Custom Mujoco Envirnonment for RL Exercises using the openai gym 
# # 

# import numpy as np 
# import os
# from gymnasium import utils 
# from gymnasium.spaces import Box
# from gymnasium.envs.mujoco import MujocoEnv
# from configparser import ConfigParser



# # Class which will bind the OpenAIs algos 
# class HealEnv(MujocoEnv): 
#     metadata = {
#         "render_modes": [
#             "human",
#             "rgb_array",
#             "depth_array",
#         ],
#         "render_fps": 100,
#     }
#     '''
#         Initialization of the mujoco environment for the robot 
#     '''
#     def __init__(self, render_mode="human"):
#         self.render_mode = render_mode 
#         configur = ConfigParser() 
#         path = os.path.dirname(os.path.abspath(__file__))
#         configPath = os.path.join(path, "config.ini")
#         configur.read(configPath)
#         rend_fps = configur.getint('Default', 'render_fps')
#         rend_path = configur.get('Default', 'path')
#         self.frame_skip = configur.getint('Default', 'skip_frame')
#         self.observation_space = Box(low = -np.inf, high = np.inf, shape = (18,), dtype = np.float64)
       
#         MujocoEnv.__init__(self, os.path.abspath(os.path.join(path,rend_path)),self.frame_skip, self.observation_space,render_mode=render_mode)
#         self.step_number = 0; 
#         self.episode_len = configur.getint('Default', 'episode_len')
#         self.init_pos = np.zeros(6)
#         self.init_vel = np.zeros(6)
#         action = np.zeros(6)
#         self.do_simulation(action, self.frame_skip)
#         min_action = configur.getfloat('Default', 'min_action')
#         max_action = configur.getfloat('Default', 'max_action')
#         bounds = self.model.actuator_ctrlrange.copy().astype(np.float64)
#         low, high = bounds.T
#         for i in range(6) : 
#             low[i] = min_action 
#             high[i] = max_action 
#         print("low = ", low)
#         print("high = ", high)
#         self.action_space = Box(low = low, high = high, dtype = np.float64)


#     '''
#         Private function to get the obs 
#     '''
#     def _get_obs(self): 
#         observation = np.zeros(18)

#         for i in range(6) : 
#             observation[i] = self.data.joint("joint_" + str(i+1)).qpos
#             observation[6+i] = self.data.joint("joint_"+str(i+1)).qvel
#             observation[12+i] = self.data.joint("joint_"+str(i+1)).qacc
        
#         return observation


#     '''
#         Reset the model with the base velocity and poses 
#     '''
#     def reset_model(self): 
#         self.step_number = 0
#         pos = self.init_pos
#         vel = self.init_vel 
#         self.set_state(pos, vel)
#         return self._get_obs()
    

#     '''
#         Perform the requisite step 
#     '''
#     def step(self, action):
#         self.do_simulation(action, self.frame_skip)
#         self.step_number+=1
#         obs = self._get_obs()
#         done = self.is_done()
#         truncated = self._is_truncated()
#         return obs, self.get_reward(),done, truncated, self._get_info()

#     '''
#         Rule when is the simulation over 
#     '''
#     def is_done(self): 
#         return False
    
#     '''
#         Whether truncated or not 
#     '''
#     def _is_truncated(self):
#         return False

#     '''
#         Get the reward 
#     '''
#     def get_reward(self):
#         return 1.0 
    
#     '''
#         Get the info 
#     '''
#     def _get_info(self):
#         return {}

import numpy as np
import os
from gymnasium import utils
from gymnasium.spaces import Box
from gymnasium.envs.mujoco import MujocoEnv
from configparser import ConfigParser

class HealEnv(MujocoEnv):
    metadata = {
        "render_modes": ["human", "rgb_array", "depth_array"],
        "render_fps": 100,
    }
    
    def __init__(self, render_mode="human"):
        self.render_mode = render_mode
        configur = ConfigParser()
        path = os.path.dirname(os.path.abspath(__file__))
        configPath = os.path.join(path, "config.ini")
        configur.read(configPath)
        rend_fps = configur.getint('Default', 'render_fps')
        rend_path = configur.get('Default', 'path')
        self.frame_skip = configur.getint('Default', 'skip_frame')
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(18,), dtype=np.float64)
        MujocoEnv.__init__(self, os.path.abspath(os.path.join(path, rend_path)), self.frame_skip, self.observation_space, render_mode=render_mode)

        # Disable gravity by setting it to zero for faster RL training
        self.model.opt.gravity[:] = 0

        self.step_number = 0
        self.episode_len = configur.getint('Default', 'episode_len')
        self.init_pos = np.zeros(6)
        self.init_vel = np.zeros(6)
        
        # Define a time-dependent trajectory as a list of joint positions over time
        self.trajectory = self.generate_trajectory()
        
        self.min_action = configur.getfloat('Default', 'min_action')
        self.max_action = configur.getfloat('Default', 'max_action')

        action = np.zeros(6)
        self.do_simulation(action, self.frame_skip)
        bounds = self.model.actuator_ctrlrange.copy().astype(np.float64)
        low, high = bounds.T
        for i in range(6):
            low[i] = self.min_action
            high[i] = self.max_action

        self.action_space = Box(low=low, high=high, dtype=np.float64)

    def _get_obs(self):
        observation = np.zeros(18)
        for i in range(6):
            observation[i] = self.data.joint("joint_" + str(i+1)).qpos
            observation[6+i] = self.data.joint("joint_" + str(i+1)).qvel
            observation[12+i] = self.data.joint("joint_" + str(i+1)).qacc
        return observation

    def generate_trajectory(self):
        """Generates a straight-line trajectory within the C-space."""
        start_position = self.init_pos  # Starting joint position (e.g., all zeros)
        end_position = np.array([0.5, 0.5, 0.0, 0.0, 0.5, 0.0])  # Target end position in C-space
        num_steps = self.episode_len

        # Create a straight line trajectory in joint space by interpolating between start and end positions
        trajectory = []
        for t in range(num_steps):
            alpha = t / (num_steps - 1)  # Interpolation factor from 0 to 1
            target_position = (1 - alpha) * start_position + alpha * end_position
            trajectory.append(target_position)

        return np.array(trajectory)

    
    def reset_model(self):
        self.step_number = 0
        pos = self.init_pos
        vel = self.init_vel
        self.set_state(pos, vel)
        return self._get_obs()

    def step(self, action):
        # Apply action to the robot's control inputs (actuators)
        self.data.ctrl[:] = action  # Set the action to the control inputs (assuming action is joint torques/velocities)
        
        # Perform the simulation with the action
        self.do_simulation(action, self.frame_skip)
        
        # Increment the step number
        self.step_number += 1
        
        # Get the new observation
        obs = self._get_obs()
        
        # Calculate reward
        reward = self.get_reward()
        
        # Check if episode is done
        done = self.is_done()
        
        # Check if episode is truncated
        truncated = self._is_truncated()
        
        return obs, reward, done, truncated, self._get_info()


    def is_done(self):
        return self.step_number >= self.episode_len

    def _is_truncated(self):
        return self.step_number >= self.episode_len

    def get_reward(self):
        # Get current joint states
        current_position = np.array([self.data.joint("joint_" + str(i+1)).qpos for i in range(6)])
        current_velocity = np.array([self.data.joint("joint_" + str(i+1)).qvel for i in range(6)])
        current_acceleration = np.array([self.data.joint("joint_" + str(i+1)).qacc for i in range(6)])
        
        # Define the target for the current time step
        target_position = self.trajectory[min(self.step_number, self.episode_len - 1)]
        
        # Position Penalty (penalize deviation from the target position)
        pos_penalty = -np.sum(np.abs(current_position - target_position))*10
        
        # Velocity Penalty (penalize deviation from zero velocity)
        vel_penalty = -np.sum(np.abs(current_velocity))
        
        # Acceleration Penalty (penalize deviation from zero acceleration)
        acc_penalty = -np.sum(np.abs(current_acceleration))
        
        # Path Reward: Reward for staying on path (closer to the target position)
        path_reward = -np.sum(np.abs(current_position - target_position))*30
        
        # Total reward, normalizing and clipping to maintain stability
        reward = (pos_penalty + vel_penalty + acc_penalty + path_reward)
        return reward

    def _get_info(self):
        return {}


