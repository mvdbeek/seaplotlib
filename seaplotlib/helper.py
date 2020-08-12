import os
import numpy as np
import seaborn as sns

from . import plt
from .styles import styles


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


def abline(slope=1, intercept=0, color=None, linetype=LINETYPE):
    """
    Plot a line from `slope` and `intercept`.

    `color` sets line color
    """
    if color is None:
        color = get_text_color()
    ax = plt.gca()
    x_vals = np.array(ax.get_xlim())
    y_vals = intercept + slope * x_vals
    ax.plot(x_vals, y_vals, linetype, color=color)


def static_abline(color=None, linetype=LINETYPE):
    if color is None:
        color = get_text_color()
    gca = plt.gca()
    gca.set_autoscale_on(False)
    gca.plot(gca.get_xlim(), gca.get_ylim(), linetype, color=color)


def save_fig_in_dir(fig, filename, directory=None, **kwargs):
    if directory is not None:
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, filename)
    fig.savefig(filename, **kwargs)


def set_style(style='white'):
    if isinstance(style, str):
        if style in styles:
            style = styles[style]
    sns.set_style(style)
    style = sns.axes_style()
    plt.rcParams['axes.facecolor'] = style['axes.facecolor']
    plt.rcParams['savefig.facecolor'] = style['axes.facecolor']


def get_text_color():
    return sns.axes_style()['text.color']
