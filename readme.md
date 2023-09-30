# Self-driven AI car
![Working](https://github.com/SmolinskiP/PatroCar/assets/49648588/1593a9f4-7ad4-4087-99d9-a38efa27e515)

Project written by creating custom [Gymnasium](https://gymnasium.farama.org/) environment.

Instructions:
1. Clone this project.
2. Use build.bat to install env (i messed some paths, and I don't have the time or inclination to correct it - .bat fixed it in no time)
3. Install dependencies (pip install pygame, gymnasium, stable_baselines3)
4. Cd into Patro_Car directory and run with "python run.py"

Environment has few attributes to modify:<br/>
game_fps (default=300) - if ```python render=True``` define speed of game clock<br/>
rotation_amount (default=6)<br/>
max_speed (default=4)<br/>
acceleration_amount (default=0.1)<br/><br/>

https://github.com/SmolinskiP/PatroCar/assets/49648588/1780c99c-4976-4fd2-a021-b11476dd157b

Great [TUTORIAL](https://www.youtube.com/watch?v=Mut_u40Sqz4&t) about this topic:<br/>

Car trained by [PPO](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html) algorithm from stable_baselines3.
