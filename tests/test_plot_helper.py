import pytest


from seaplotlib.helper import (
    abline,
    despine,
    static_abline,
    set_style,
)


@pytest.mark.parametrize('color', ['k', 'r'])
@pytest.mark.mpl_image_compare
def test_abline(default_image, color):
    abline(intercept=0, slope=1, color=color)
    return default_image.figure


@pytest.mark.parametrize('color', ['k', 'r'])
@pytest.mark.mpl_image_compare
def test_static_abline(default_image, color):
    static_abline(color=color)
    return default_image.figure


@pytest.mark.mpl_image_compare
def test_despine(default_image):
    despine(default_image)
    return default_image.figure


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize('style', [None, 'black', 'white'])
def test_style(default_dataframe, style):
    set_style(style)
    ax = default_dataframe.plot(kind='scatter', x=0, y=1)
    return ax.figure
