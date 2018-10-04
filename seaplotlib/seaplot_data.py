import numpy as np
import seaborn as sns


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
            legend=False,
            **kwargs)


class MaPlotData(DataDescription, CanDisplayScatter):

    """Simplfies MaPlot'ing."""

    def __init__(self, df, highlight_in=None, label_in=None):
        super(MaPlotData, self).__init__(df=df)
        self._xlabel = 'log2(Base mean)'
        self._ylabel = 'log2(FC)'
        self.highlight_in = highlight_in
        self.label_in = label_in

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
            self.data['highlight_in'] = self.data.index.isin(self.highlight_in)
            return 'highlight_in'
        return None


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
