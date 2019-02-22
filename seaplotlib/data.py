import numpy as np
import seaborn as sns
from matplotlib.font_manager import FontProperties

class DataDescription(object):

    def __init__(self, df):
        self.data = df


class CanDisplayScatter(object):
    """Can be displayed as scatterplot without conversion."""

    def plot_scatterplot(self, **kwargs):
        return sns.scatterplot(
            x=self.x,
            y=self.y,
            hue=self.hue,
            data=self.data,
            legend=kwargs.pop('legend', False),
            **kwargs)


class CanDisplayLabel(object):

    def plot_label(self, ax, **kwargs):
        data = self.data
        highlight_in = self.highlight_in
        label_in = self.label_in
        default_label_color = sns.axes_style()['text.color']
        font0 = FontProperties()
        font0.set_weight('bold')
        for idx in data.index:
            if idx in highlight_in:
                color = default_label_color
                if hasattr(self, 'highlight_text_color') and self.highlight_text_color is not None:
                    color = self.highlight_text_color
            if (isinstance(label_in, str) and label_in == 'all') or idx in set(label_in) or (idx in highlight_in and self.label_highlight):
                if isinstance(label_in, dict):
                    label = label_in[idx]
                else:
                    label = idx
                x = self.data.loc[idx][self.x]
                y = self.data.loc[idx][self.y]
                ax.annotate(label, xy=(x, y),
                            xytext=(x + 0.4, y + 0.2),
                            arrowprops=dict(facecolor='black', shrink=0.05),
                            )
        return ax


class MaPlotData(DataDescription, CanDisplayScatter, CanDisplayLabel):

    """Simplfies MaPlot'ing."""

    def __init__(self, df, highlight_in=None, label_in=None, label_highlight=False, highlight_label=None, highlight_text_color=None):
        super(MaPlotData, self).__init__(df=df)
        self._xlabel = 'log2(Base mean)'
        self._ylabel = 'log2(FC)'
        self.highlight_in = highlight_in
        self.label_in = label_in
        self.label_highlight = label_highlight
        self.highlight_label = highlight_label
        self.highlight_text_color = highlight_text_color

    @property
    def x(self):
        self.data[self.xlabel] = np.log2(self.data['Base mean'])
        return self.xlabel

    @property
    def y(self):
        return self._ylabel

    @property
    def xlabel(self):
        return self._xlabel

    @property
    def ylabel(self):
        return self._ylabel

    @property
    def significance(self):
        return 'P-adj'

    @property
    def hue(self):
        if self.highlight_in:
            highlight_label = self.highlight_label or 'highlight_in'
            self.data[highlight_label] = self.data.index.isin(self.highlight_in)
            return highlight_label
        return None


class VolcanoPlotData(MaPlotData):

    def __init__(self, df, highlight_in=None, label_in=None, label_highlight=False, highlight_label=None):
        super(VolcanoPlotData, self).__init__(df=df, highlight_in=highlight_in, label_in=label_in, label_highlight=label_highlight, highlight_label=highlight_label)
        self._xlabel = 'log2(FC)'
        self._ylabel = 'P-adj'

    @property
    def x(self):
        return self.xlabel

    @property
    def y(self):
        self.data[self.ylabel] = -np.log10(self.data[self._ylabel])
        return self.ylabel

    @property
    def ylabel(self):
        return '-log10(P-adj)'


class TwoColumnScatterData(MaPlotData):

    def __init__(self, df, highlight_in=None, label_in=None, logx=None, logy=None):
        super(TwoColumnScatterData, self).__init__(df=df, highlight_in=highlight_in, label_in=label_in)
        self.logx = logx
        self.logy = logy
        self._xlabel = self.data.columns[1]
        self._ylabel = self.data.columns[0]

    @property
    def _transformed_xlabel(self):
        if self.logx:
            xlabel = "{logx}({xlabel})".format(logx=self.logx, xlabel=self.xlabel)
            self.data[xlabel] = getattr(np, self.logx)(self.data[self._xlabel])
            return xlabel
        return None

    @property
    def _transformed_ylabel(self):
        if self.logx:
            ylabel = "{logy}({ylabel})".format(logy=self.logx, ylabel=self.ylabel)
            self.data[ylabel] = getattr(np, self.logy)(self.data[self._ylabel])
            return ylabel
        return None

    @property
    def x(self):
        return self._transformed_xlabel or self._xlabel

    @property
    def y(self):
        return self._transformed_ylabel or self._ylabel
