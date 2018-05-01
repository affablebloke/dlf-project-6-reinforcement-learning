import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_point(axis, x, y, z, **kwargs):
    axis.scatter([x], [y], [z], **kwargs)
    axis.text(x, y, z, "({:.1f}, {:.1f}, {:.1f})".format(x, y, z))


def plot_flight(path, target, figsize=(20, 20)):
    fig = plt.figure(figsize=figsize)
    axis = fig.gca(projection='3d')
    axis.set_xlabel('X-axis')
    axis.set_ylabel('Y-axis')
    axis.set_zlabel('Z-axis')
    axis.plot3D(path['x'], path['y'], path['z'], 'gray')
    plot_point(axis, target[0], target[1], target[2], c='blue', marker='x', s=100, label='target')
    plot_point(axis, path['x'][0], path['y'][0], path['z'][0], c='green', marker='o', s=50, label='start')
    plot_point(axis, path['x'][-1], path['y'][-1], path['z'][-1], c='red', marker='o', s=50, label='end')
    axis.legend()
    return axis
