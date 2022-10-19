import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
import seaborn as sns

from config import *


def plotter(coordinates):
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    cmap = ListedColormap(sns.color_palette(
        COLOR_PALETTE, len(TELLO_IP_ADDRESSES)).as_hex())

    def animate(i):
        try:
            x = [d['x'] for d in coordinates]
            y = [d['y'] for d in coordinates]
            z = [d['z'] for d in coordinates]
            tello_i = [d['tello'] for d in coordinates]
        except (BrokenPipeError, TypeError):
            return

        plt.cla()

        # draw tello path
        # TODO: draw lines instead of points. Problem: how to do it efficiently with multiple tellos?
        ax.scatter3D(
            x,
            y[:len(x)],
            z[:len(x)],
            s=PATH_MARKER_RADIUS, c=tello_i[:len(x)], cmap=cmap, alpha=0.9
        )

        # draw tello itself
        ax.scatter3D(
            x[len(x)-1:len(x)],
            y[len(x)-1:len(x)],
            z[len(x)-1:len(x)],
            s=TELLO_MARKER_RADIUS, c=tello_i[len(x)-1:len(x)], cmap=ListedColormap(TELLO_MARKER_COLORS), alpha=1
        )
        plt.draw()

    ani = FuncAnimation(plt.gcf(), animate, interval=PLOT_UPDATE_INTERVAL)

    plt.show()
