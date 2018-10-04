import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


DEFAULT_ABLINE_COLOR = 'k'
LINETYPE = '--'


def despine(ax):
    """
    Despine an ax object.
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return ax


def abline(slope=1, intercept=0, color=DEFAULT_ABLINE_COLOR, linetype=LINETYPE):
    """
    Plot a line from `slope` and `intercept`.

    `color` sets line color
    """
    # plt.autoscale(tight=True)
    ax = plt.gca()
    x_vals = np.array(ax.get_xlim())
    y_vals = intercept + slope * x_vals
    ax.plot(x_vals, y_vals, linetype, color=color)


def static_abline(color=DEFAULT_ABLINE_COLOR, linetype=LINETYPE):
    gca = plt.gca()
    gca.set_autoscale_on(False)
    gca.plot(gca.get_xlim(), gca.get_ylim(), linetype, color=color)
