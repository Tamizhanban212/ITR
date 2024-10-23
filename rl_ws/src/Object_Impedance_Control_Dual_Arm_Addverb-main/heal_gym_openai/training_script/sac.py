# '''
# # Author : Rajesh Kumar (rajesh.kumar01@addverb.com)
# # Details : This is the OpenAI SAC example for the heal robot 
# '''

# import registration
# import gymnasium as gym 

# from stable_baselines3.sac.policies import MlpPolicy
# from stable_baselines3 import SAC 


# env = gym.make("Heal-v1", render_mode="human") 

# # default device is cuda 
# model = SAC("MlpPolicy", env, verbose = 1)

# model.learn(total_timesteps=50000, log_interval=10)

# model.save("heal_cobot")

# env = model.get_env()
# obs = env.reset()

# while True:
#     action, _states = model.predict(obs)

#     obs, rewards, dones, info = env.step(action)
#     env.render("human")

# sac.py
import gymnasium as gym
from stable_baselines3 import SAC
import registration

# Create the environment
env = gym.make("Heal-v1", render_mode="human")

# Initialize the SAC model
model = SAC(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=1e-4,  # Lower learning rate
    batch_size=256,
    gamma=0.99,
    tau=0.005,
    ent_coef='auto',
    train_freq=1,
    gradient_steps=1,
    buffer_size=1000000,
    device="cuda"
)


# Train the model
model.learn(total_timesteps=50000, log_interval=10)

# Save the trained model
model.save("heal_sac")

# Close the environment
env.close()
