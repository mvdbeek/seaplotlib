from functools import wraps
from .helper import abline
from .seaplotlib import plt


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
            abline()
        return r
    return _abline


def tight_layout(function):
    @wraps(function)
    def tight_layout(*args, **kwargs):
        r = function(*args, **kwargs)
        plt.tight_layout()
        return r
    return tight_layout
