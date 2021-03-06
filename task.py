import numpy as np

from physics_sim import PhysicsSim


class Task():
    """Task (environment) that defines the goal and provides feedback to the agent."""

    def __init__(self, init_pose=None, init_velocities=None,
                 init_angle_velocities=None, runtime=5., target_pos=None, action_repeat=1):
        """Initialize a Task object.
        Params
        ======
            init_pose: initial position of the quadcopter in (x,y,z) dimensions and the Euler angles
            init_velocities: initial velocity of the quadcopter in (x,y,z) dimensions
            init_angle_velocities: initial radians/second for each of the three Euler angles
            runtime: time limit for each episode
            target_pos: target/goal (x,y,z) position for the agent
        """
        # Simulation

        self.sim = PhysicsSim(init_pose, init_velocities,
                              init_angle_velocities, runtime)
        self.action_repeat = action_repeat
        self.init_pose = init_pose
        self.state_size = self.action_repeat * 6
        self.action_low = 0.
        self.action_high = 900.
        self.action_size = 4

        # Goal
        self.target_pos = target_pos if target_pos is not None else np.array([
                                                                             0., 0., 10.])

    def vector_magnitude(self, v):
        return np.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) + 0.00001

    def unit_vector(self, v):
        return v / self.vector_magnitude(v)

    def hover_unit_vector(self):
        return np.array([0., 0., 1.0])

    def get_position_reward(self):
        return -abs(self.sim.pose[:3] - self.target_pos).sum() / 300.0

    def get_drift_xy_plane_reward(self):
        return -abs(self.sim.pose[:2] - self.target_pos[:2]).sum() / 300.00

    def penalize_failed_runtime(self):
        reward = 0.0
        if self.sim.time < self.sim.runtime and self.sim.done:
            reward = -10.0
        return reward

    def get_reward(self):
        """Uses current pose of sim to return reward."""
        reward = self.get_position_reward()
        reward += self.penalize_failed_runtime()
        return reward

    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            # update the sim pose and velocities
            done = self.sim.next_timestep(rotor_speeds)
            reward += self.get_reward()
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate([self.sim.pose] * self.action_repeat)
        return state
