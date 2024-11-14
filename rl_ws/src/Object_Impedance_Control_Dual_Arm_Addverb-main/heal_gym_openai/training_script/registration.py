'''
# Author : Rajesh Kumar (rajesh.kumar01@addverb.com)
# Perform all the initializations 
'''

import os 
import sys 
import gymnasium as gym 
import numpy as np
sys.path.append('/home/tamizhanban/Documents/ITR/rl_ws/src/Object_Impedance_Control_Dual_Arm_Addverb-main/heal_gym_openai')

from env.heal_env import HealEnv

from gymnasium.envs.registration import register

register(
    id="Heal-v1",
    # path to the class for creating the env
    # Note: entry_point also accept a class as input (and not only a string)
    entry_point="env.heal_env:HealEnv",
    # Max number of steps per episode, using a `TimeLimitWrapper`
    max_episode_steps=5000,
)
