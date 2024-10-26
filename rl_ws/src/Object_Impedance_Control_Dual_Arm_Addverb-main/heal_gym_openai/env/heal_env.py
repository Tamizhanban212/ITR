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
        
        self.step_number = 0
        self.episode_len = configur.getint('Default', 'episode_len')
        self.init_pos = np.zeros(6)
        self.init_vel = np.zeros(6)
        self.target_joint_state = np.array([0.5, 0.5, 0.0, 0.0, 0.5, 0.0])  # Target positions for the last two joints
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

    def reset_model(self):
        self.step_number = 0
        pos = self.init_pos
        vel = self.init_vel
        self.set_state(pos, vel)
        return self._get_obs()

    def step(self, action):
        self.do_simulation(action, self.frame_skip)
        self.step_number += 1
        obs = self._get_obs()
        reward = self.get_reward()
        done = self.is_done()
        truncated = self._is_truncated()
        return obs, reward, done, truncated, self._get_info()

    def is_done(self):
        info = self._get_info()
        loss = info.get("loss", 1.0)  # Default to 1.0 if loss is not found
        return np.abs(loss) < 1

    def _is_truncated(self):
        info = self._get_info()
        loss = info.get("loss", 1.0)  # Default to 1.0 if loss is not found
        return np.abs(loss) < 1

    def get_reward(self):
        current_joint_state = np.array([self.data.joint("joint_" + str(i+1)).qpos for i in range(6)])
        diff = np.abs(current_joint_state - self.target_joint_state)
        reward = -np.sum(diff)  # Negative sum of differences between current and target states
        
        # Normalizing the reward
        reward = np.clip(reward / 6.0, -1, 1)
        
        return reward

    def _get_info(self):
        return {}

