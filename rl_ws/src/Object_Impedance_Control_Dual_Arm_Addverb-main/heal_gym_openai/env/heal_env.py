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

# heal_env.py
# Author : Rajesh Kumar (rajesh.kumar01@addverb.com)
# Details : Custom Mujoco Environment for RL Exercises using the OpenAI gym

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
        configPath = os.path.join(path, "config.ini")
        configur.read(configPath)

        self.frame_skip = configur.getint('Default', 'skip_frame')
        self.episode_len = configur.getint('Default', 'episode_len')
        self.step_number = 0

        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(18,), dtype=np.float64)

        # Read min_action and max_action from the config file
        min_action = configur.getfloat('Default', 'min_action')
        max_action = configur.getfloat('Default', 'max_action')

        # Set the action space with defined range
        self.action_space = Box(low=min_action, high=max_action, shape=(6,), dtype=np.float64)

        MujocoEnv.__init__(self, os.path.abspath(os.path.join(path, configur.get('Default', 'path'))),
                           self.frame_skip, self.observation_space, render_mode=render_mode)

        self.init_pos = np.zeros(6)
        self.init_vel = np.zeros(6)
        self.target_position = np.array([0, 0, 0, 0, 1.5, 1.5])
        self.max_position_error = 0.05  # Threshold for considering the task done

    def _get_obs(self):
        observation = np.concatenate([
            self.data.qpos.flat[:6] / np.pi,  # Normalize joint positions
            self.data.qvel.flat[:6] / 10.0,   # Normalize velocities
            self.data.qacc.flat[:6] / 100.0   # Normalize accelerations
        ])
        return observation

    def reset_model(self):
        self.step_number = 0
        self.init_pos = np.random.uniform(low=-0.1, high=0.1, size=6)
        self.init_vel = np.zeros(6)
        self.set_state(self.init_pos, self.init_vel)

        # Set target positions based on the actuator control range
        bounds = self.model.actuator_ctrlrange.copy().astype(np.float64)
        low, high = bounds.T
        self.target_position = np.random.uniform(low=low, high=high, size=6)
        
        return self._get_obs()

    # def step(self, action): # PPO
    #     self.do_simulation(action, self.frame_skip)
    #     self.step_number += 1
    #     obs = self._get_obs()
    #     done = self.is_done()
    #     truncated = self._is_truncated()
    #     reward = self.get_reward()
    #     info = self._get_info()
    #     return obs, reward, done, truncated, info

    def step(self, action): # SAC
        # Clip the action to the valid range
        action = np.clip(action, self.action_space.low, self.action_space.high)
        self.do_simulation(action, self.frame_skip)
        self.step_number += 1
        obs = self._get_obs()
        done = self.is_done()
        truncated = self._is_truncated()
        reward = self.get_reward()
        info = self._get_info()
        return obs, reward, done, truncated, info

    def is_done(self):
        # Check if the current position is close enough to the target position
        current_position = self.data.qpos[:6]
        position_error = np.linalg.norm(current_position - self.target_position)
        if position_error < self.max_position_error:
            return True
        # Also consider the maximum number of steps for termination
        return self.step_number >= self.episode_len

    def _is_truncated(self):
        # Truncate the episode if it exceeds the predefined episode length
        return self.step_number >= self.episode_len

    # def get_reward(self): # PPO
    #     current_position = self.data.qpos[:6]
    #     distance_to_target = np.linalg.norm(current_position - self.target_position)
    #     reward = -distance_to_target  # Negative reward for distance
    #     if distance_to_target < self.max_position_error:
    #         reward += 10.0  # Bonus for reaching the target
    #     return reward
    
    def get_reward(self): # SAC
        current_position = self.data.qpos[:6]
        distance_to_target = np.linalg.norm(current_position - self.target_position)
        # Scale and clip the reward
        reward = -distance_to_target
        reward = np.clip(reward, -1.0, 1.0)  # Clip the reward between -1.0 and 1.0
        if distance_to_target < self.max_position_error:
            reward += 10.0  # Bonus for reaching the target
        return reward

    def _get_info(self):
        # Provide information about the current distance to the target
        current_position = self.data.qpos[:6]
        distance_to_target = np.linalg.norm(current_position - self.target_position)
        return {
            "distance_to_target": distance_to_target,
            "target_position": self.target_position,
        }
