import numpy as np

from task import Task


class HoverTask(Task):
    def __init__(self):
        target_pos = np.array([0., 0., 10.])
        init_pos = np.array([0., 0., 10., 0., 0., 0.])
        super(HoverTask, self).__init__(action_repeat=1,
                                        init_pose=init_pos, target_pos=target_pos, runtime=5.)
        self.action_low = 0.
        self.action_high = 900.

    def get_reward(self):
        total_dist = np.linalg.norm(self.target_pos[:3]-self.sim.pose[:3])
        # dist_xy_plane = np.linalg.norm(self.target_pos[:2]-self.sim.pose[:2])
        # dist_z = np.linalg.norm(self.target_pos[2]-self.sim.pose[2])
        # reward -= total_dist / 5.0
        # reward -= dist_xy_plane / 10.0
        # reward += self.sim.v[2] / 20.0
        # reward -= np.tanh(abs(self.sim.v[0]))
        # reward -= np.tanh(abs(self.sim.v[1]))
        # reward -= total_dist / 300.0
        # if self.sim.time < self.sim.runtime and self.sim.done:
        #     reward -= self.sim.runtime - self.sim.time
        reward = -(total_dist / 20.0)
        reward += self.sim.v[2] / 4.0
        return np.tanh(reward)

    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            # update the sim pose and velocities
            done = self.sim.next_timestep(rotor_speeds)
            total_dist = np.linalg.norm(self.target_pos[:3]-self.sim.pose[:3])
            if total_dist > 5.0:
                done = True
                reward += -1
            else:
                reward += self.get_reward()
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done
