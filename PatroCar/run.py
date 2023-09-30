import race_track
import gymnasium as gym
from time import sleep

import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold

log_path = os.path.join('Training', 'Logs')
PPO_Path = os.path.join('Training', 'Saved Models', 'Race_track_007')

env = gym.make('race_track/RaceTrack-v0', render_mode="human", game_fps=300, rotation_amount=6, max_speed=4, acceleration_amount=0.1)
#env = gym.make('race_track/RaceTrack-v0', game_fps=60, rotation_amount=6, max_speed=5, acceleration_amount=0.1)

#env = DummyVecEnv([lambda: env])
#env = SubprocVecEnv([lambda: env])

#eval_callback = EvalCallback(env, eval_freq=10000, best_model_save_path=os.path.join('Training', 'Saved Models'), verbose=1)

def learn_car(initialize_model=False, timesteps=2000, loops=True):
    if initialize_model == True:
        model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_path)
        env.reset()
        model.learn(total_timesteps=timesteps)
        model.save(PPO_Path)
        print(model.learning_rate)
    else:
        model = PPO.load(PPO_Path, env=env, render=True)
        if loops == True:
            while True:
                env.reset()
                model.learn(total_timesteps=timesteps)
                model.save(PPO_Path)
                print(model.learning_rate)
        else:
            i = 0
            while i < loops:
                env.reset()
                model.learn(total_timesteps=timesteps)
                model.save(PPO_Path)
                i+=1
                print(model.learning_rate)
                
    
                
def check_car(episodes=5):
    episodes = episodes
    model = PPO.load(PPO_Path, env=env)
    for episode in range (0, episodes):
        obs = env.reset()[0]
        donee = 0
        score = 0
    
        while donee < 50000:
            #env.render()
            action = model.predict(obs)
            obs, reward, done, info, dupa = env.step(action[0])
            score += reward
            donee += 1
        print("CUMULATIVE REWARD: %s" % score)
    env.close()

learn_car(initialize_model=True)
#learn_car(loops=3)
learn_car(timesteps=5000)
#check_car()

# model = PPO.load(PPO_Path, env=env)
# print(evaluate_policy(model, env, n_eval_episodes=1, render=True))

