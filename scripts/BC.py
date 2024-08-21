import numpy as np
from stable_baselines3.common.evaluation import evaluate_policy

from imitation.algorithms import bc
from imitation.data import rollout
from imitation.data.wrappers import RolloutInfoWrapper
from imitation.policies.serialize import load_policy
from imitation.util.util import make_vec_env
from imitation.data.types import Trajectory

from cathsim_controller.real_env import RealEnv
from experience_read import read_as_trajectory

FPS = 8
WIDTH = 1920
HEIGHT = 1080

# read the expert episodes
# expert_episodes=read(num=20,start_id=1)

# Convert your expert data to Trajectory objects
trajectories = read_as_trajectory(num=2,start_id=21)
print(trajectories)
transitions = rollout.flatten_trajectories(trajectories)
print("I am here")

# Envronment
env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)
env.reset()

rng = np.random.default_rng(0)
observation_space=env.observation_space
print(observation_space.sample())
bc_trainer = bc.BC(
    observation_space=env.observation_space,
    action_space=env.action_space,
    demonstrations=transitions,
    rng=rng,
)
bc_trainer.train(n_epochs=1)
reward, _ = evaluate_policy(bc_trainer.policy, env, 10)
print("Reward:", reward)