from seaplotlib.data import (
    MaPlotData,
    TwoColumnScatterData,
)


def test_maplot_data(deseq_data):
    data = MaPlotData(df=deseq_data)
    assert data.xlabel == 'log2(Base mean)'
    assert data.ylabel == 'log2(FC)'
    assert data.significance == 'P-adj'
    assert data.x == 'log2(Base mean)'
    assert data.y == 'log2(FC)'
    assert data.hue is None
    data.highlight_in = ('pogo',)
    assert data.hue == 'highlight_in'


def test_two_column_scatter_data(two_column_data):
    data = TwoColumnScatterData(df=two_column_data)
    assert "c1", "c2" == data.data.columns
    assert data.xlabel == 'c2'
    assert data.ylabel == 'c1'
    assert data.significance == 'P-adj'
    assert data.x == 'c2'
    assert data.y == 'c1'
    assert data.hue is None
    data.highlight_in = ('pogo',)
    assert data.hue == 'highlight_in'
