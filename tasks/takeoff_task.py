import numpy as np

from task import Task


class TakeoffTask(Task):
    def __init__(self):
        target_pos = np.array([0., 0., 100.])
        init_pos = np.array([0., 0., 1., 0., 0., 0.])
        super(TakeoffTask, self).__init__(init_pose=init_pos,
                                          target_pos=target_pos, runtime=5.)
        self.action_low = 0.0
        self.action_high = 900.0
        self.action_repeat = 1

    def get_reward(self):
        total_dist = np.linalg.norm(self.target_pos[:3]-self.sim.pose[:3])
        reward = self.sim.v[2] / 20.0
        reward -= 100.0 - total_dist
        # TODO: normalize this reward between -1.0 and 1.0. Otherwise it gets stuck with the rewards
        return np.tanh(reward)

    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            # update the sim pose and velocities
            done = self.sim.next_timestep(rotor_speeds)
            total_dist = np.linalg.norm(self.target_pos[:3]-self.sim.pose[:3])
            if total_dist > 150.0:
                done = True
                reward += -1
            else:
                reward += self.get_reward()
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done
