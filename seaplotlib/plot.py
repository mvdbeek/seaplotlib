from . import decorators as dec

from .helper import (
    despine,
    get_text_color,
)
from .data import (
    MaPlotData,
    TwoColumnScatterData,
    VolcanoPlotData,
)


@dec.tight_layout
@dec.can_set_title
@dec.can_set_xlabel
@dec.can_set_ylabel
@dec.can_add_abline
@dec.can_set_equal_scale
@dec.can_create_figure
def two_column_plot(df, ax, highlight_in=(), label_in=(), logx=None, logy=None):
    data = TwoColumnScatterData(df=df, highlight_in=highlight_in, label_in=label_in, logx=logx, logy=logy)
    ax = data.plot_scatterplot(ax=ax)
    ax = data.plot_label(ax=ax)
    despine(ax)
    return ax


@dec.can_set_title
@dec.can_set_xlabel
@dec.can_set_ylabel
@dec.can_create_figure
def maplot_deseq2(df, ax, highlight_in=(), label_in=(), **kwargs):
    """Generate maplot."""
    data = MaPlotData(df, label_in=label_in, highlight_in=highlight_in)
    ax = despine(data.plot_scatterplot(ax=ax, **kwargs))
    ax = data.plot_label(ax=ax)
    ax.axhline(color=get_text_color())
    return ax


@dec.can_set_title
@dec.can_set_xlabel
@dec.can_set_ylabel
@dec.can_create_figure
def volcano_deseq2(df, ax, highlight_in=(), label_in=(), scatter_kwargs={}, highlight_label=None):
    data = VolcanoPlotData(df=df, highlight_in=highlight_in, label_in=label_in, highlight_label=highlight_label)
    ax = data.plot_scatterplot(ax=ax, **scatter_kwargs)
    ax = data.plot_label(ax=ax)
    despine(ax)
    ax.set_ylim(0)
    ax.axvline(color=get_text_color(), label='_nolegend_')
    return ax
