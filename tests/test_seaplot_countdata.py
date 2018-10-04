import pytest

from seaplotlib import plot


@pytest.mark.parametrize('title,xlabel,ylabel', [
    (None, None, None),
    ('title', 'xlabel', 'ylabel')
])
@pytest.mark.mpl_image_compare
def test_maplot_deseq2(deseq_data, title, xlabel, ylabel):
    return plot.maplot_deseq2(df=deseq_data,
                           highlight_in=('pogo',),
                           label_in='all',
                           title=title,
                           xlabel=xlabel,
                           ylabel=ylabel).figure


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize('title,xlabel,ylabel,logx,logy,equal_scale,abline', [
    (None, None, None, None, None, None, False),
    ('title', 'xlabel', 'ylabel', 'log2', 'log2', True, True),
    ('log10 title', None, None, 'log10', 'log10', True, True),
])
def test_two_column_plot(two_column_data, title, xlabel, ylabel, logx, logy, equal_scale, abline):
    return plot.two_column_plot(df=two_column_data,
                             highlight_in=('pogo',),
                             label_in='all',
                             title=title,
                             xlabel=xlabel,
                             ylabel=ylabel,
                             logx=logx,
                             logy=logy,
                             equal_scale=equal_scale,
                             abline=abline,
                             ).figure


@pytest.mark.mpl_image_compare
def test_volcano(deseq_data):
    return plot.volcano_deseq2(df=deseq_data).figure
