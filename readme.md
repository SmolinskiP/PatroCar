# Self-driven AI car

**Self-Driven AI Car** is a project that simulates an autonomous car using a custom environment built with Gymnasium. The car is trained using the PPO algorithm from the stable_baselines3 library, providing an interactive and customizable experience for AI enthusiasts.


![Working](https://github.com/SmolinskiP/PatroCar/assets/49648588/1593a9f4-7ad4-4087-99d9-a38efa27e515)

Project written by creating custom [Gymnasium](https://gymnasium.farama.org/) environment.

## Instructions

1. **Clone this project.**
2. **Install the environment** using `build.bat` (it fixes some path issues that I didn't have time to resolve manually).
3. **Install dependencies:**
   ```bash
   pip install pygame gymnasium stable_baselines3
   ```
4. **Edit the `run.py` file** according to your needs.
5. **Navigate to the Patro_Car directory** and run:
   ```bash
   python run.py
   ```

## Customizable Environment Attributes:

- **game_fps** (default=300): Controls the game clock speed if `render_mode="human"` is set.
- **rotation_amount** (default=6): Defines how much the car rotates.
- **max_speed** (default=4): Sets the maximum speed of the car.
- **acceleration_amount** (default=0.1): Determines the car's acceleration rate.

## Additional Resources

https://github.com/SmolinskiP/PatroCar/assets/49648588/1780c99c-4976-4fd2-a021-b11476dd157b

Great [TUTORIAL](https://www.youtube.com/watch?v=Mut_u40Sqz4&t) about this topic:<br/>

Car trained by [PPO](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html) algorithm from stable_baselines3.
