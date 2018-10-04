import pytest


from seaplotlib.plot_helper import (
    abline,
    despine,
    static_abline,
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
