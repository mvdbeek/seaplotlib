from functools import wraps

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import seaborn as sns  # noqa: E402

from .plot_helper import (  # noqa: E402
    abline,
    despine,
)
from .seaplot_data import (  # noqa: E402
    MaPlotData,
    TwoColumnScatterData,
    VolcanoPlotData,
)
from .styles import styles  # noqa: E402


def can_set_title(function):
    @wraps(function)
    def set_title(*args, **kwargs):
        title = kwargs.pop('title', None)
        r = function(*args, **kwargs)
        if title:
            ax = plt.gca()
            ax.set_title(title)
        return r
    return set_title


def can_set_xlabel(function):
    @wraps(function)
    def set_xlabel(*args, **kwargs):
        xlabel = kwargs.pop('xlabel', None)
        r = function(*args, **kwargs)
        if xlabel:
            ax = plt.gca()
            ax.set_xlabel(xlabel)
        return r
    return set_xlabel


def can_set_ylabel(function):
    @wraps(function)
    def set_ylabel(*args, **kwargs):
        ylabel = kwargs.pop('ylabel', None)
        r = function(*args, **kwargs)
        if ylabel:
            ax = plt.gca()
            ax.set_ylabel(ylabel)
        return r
    return set_ylabel


def can_create_figure(function):
    @wraps(function)
    def create_figure(*args, **kwargs):
        if not kwargs.get('ax'):
            figsize = kwargs.pop('figsize', None)
            _, kwargs['ax'] = plt.subplots(figsize=figsize)
        return function(*args, **kwargs)

    return create_figure


def can_set_equal_scale(function):
    @wraps(function)
    def set_equal_scale(*args, **kwargs):
        equal_scale = kwargs.pop('equal_scale', False)
        r = function(*args, **kwargs)
        if equal_scale:
            ax = plt.gca()
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            new_min = min(xlim[0], ylim[0])
            new_max = max(xlim[1], ylim[1])
            assert (new_min, new_max) == ax.set_xlim(new_min, new_max)
            assert (new_min, new_max) == ax.set_ylim(new_min, new_max)
        return r

    return set_equal_scale


def can_add_abline(function):
    @wraps(function)
    def _abline(*args, **kwargs):
        add_abline = kwargs.pop('abline', False)
        r = function(*args, **kwargs)
        if add_abline:
            abline(color=args[0].abline_color)
        return r
    return _abline


def tight_layout(function):
    @wraps(function)
    def tight_layout(*args, **kwargs):
        r = function(*args, **kwargs)
        plt.tight_layout()
        return r
    return tight_layout


class CountPlot(object):
    def __init__(self, style='white'):
        if isinstance(style, str):
            if style in styles:
                style = styles[style]
        sns.set_style(style)
        self.style = sns.axes_style()
        matplotlib.pyplot.rcParams['axes.facecolor'] = self.style['axes.facecolor']
        matplotlib.pyplot.rcParams['savefig.facecolor'] = self.style['axes.facecolor']
        self.abline_color = self.style['text.color']
        self.label_color = self.style['text.color']

    def label_plot(self, df, ax, x, y, highlight=('rover',), label='all'):
        for idx in df.index:
            if idx in highlight:
                color = 'r'
            else:
                color = self.label_color
            if (isinstance(label, str) and label == 'all') or idx in label or idx in highlight:
                ax.text(df.loc[idx][x], df.loc[idx][y], idx, color=color)

    @tight_layout
    @can_set_title
    @can_set_xlabel
    @can_set_ylabel
    @can_add_abline
    @can_set_equal_scale
    @can_create_figure
    def two_column_plot(self, df, ax, highlight_in=(), label_in=(), logx=None, logy=None):
        data = TwoColumnScatterData(df=df, highlight_in=highlight_in, label_in=label_in, logx=logx, logy=logy)
        ax = data.plot_scatterplot(ax=ax)
        despine(ax)
        self.label_plot(df=data.data, ax=ax, x=data.x, y=data.y, highlight=data.highlight_in, label=data.label_in)
        return ax

    @can_set_title
    @can_set_xlabel
    @can_set_ylabel
    @can_create_figure
    def maplot_deseq2(self, df, ax, highlight_in=(), label_in=()):
        """Generate maplot."""
        mpd = MaPlotData(df, label_in=label_in, highlight_in=highlight_in)
        ax = despine(mpd.plot_scatterplot(ax=ax))
        ax.axhline(color=self.abline_color)
        self.label_plot(df=mpd.data, ax=ax, x=mpd.x, y=mpd.y, highlight=mpd.highlight_in, label=mpd.label_in)
        return ax

    @can_set_title
    @can_set_xlabel
    @can_set_ylabel
    @can_create_figure
    def volcano_deseq2(self, df, ax, highlight_in=(), label_in=()):
        data = VolcanoPlotData(df=df, highlight_in=highlight_in, label_in=label_in)
        ax = data.plot_scatterplot(ax=ax)
        despine(ax)
        self.label_plot(df=data.data, ax=ax, x=data.x, y=data.y, highlight=data.highlight_in, label=data.label_in)
        ax.set_ylim(0)
        ax.axvline(color=self.abline_color)
        return ax
