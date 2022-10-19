# Ip addresses of tellos to connect.
TELLO_IP_ADDRESSES = [
    "192.168.10.1",
]

# Initial coordinates of tellos in positioner and in plotter.
# Order of tellos as in TELLO_IP_ADDRESSES.
INITIAL_X = [0]
INITIAL_Y = [0]

# Interval for which the positions will be updated. Value in seconds.
POSITIONER_INTERVAL = 0.005

# Interval for which the plot will be updated. Value in milliseconds.
PLOT_UPDATE_INTERVAL = 50

# Radius of scattered points of path in the plot.
PATH_MARKER_RADIUS = 5

# Radius of the marker representing current position of the tello.
TELLO_MARKER_RADIUS = 100

# Color of the markers representing current position of the tello.
# Order of tellos as in TELLO_IP_ADDRESSES.
TELLO_MARKER_COLORS = ['#F00']

'''
COLOR_PALETTE : None, string, or sequence
        Name of palette or None to return current palette. If a sequence, input
        colors are used but possibly cycled and desaturated.
------------------------------------------------------------------------------------
Possible ``COLOR_PALETTE`` values include:
        - Name of a seaborn palette (deep, muted, bright, pastel, dark, colorblind)
        - Name of matplotlib colormap
        - 'husl' or 'hls'
        - 'ch:<cubehelix arguments>'
        - 'light:<color>', 'dark:<color>', 'blend:<color>,<color>',
        - A sequence of colors in any format matplotlib accepts

    Setting ``COLOR_PALETTE=None`` will use the current matplotlib color cycle.

    See the :ref:`tutorial <palette_tutorial>` for more information.

'''
COLOR_PALETTE = 'bright'
