import pytest

import pandas as pd


@pytest.fixture
def default_dataframe():
    return pd.DataFrame.from_dict({1: [1, 2], 2: [2, 4], 4: [4, 4]}, orient='index')


@pytest.fixture
def two_column_data():
    return pd.DataFrame.from_dict({
        'c1': {'copia': 228474.90148541998,
               'TART-C': 7196.620779259613,
               '3S18': 10923.199852531354,
               'springer': 3144.986489182313,
               'accord': 2560.9006022481035},
        'c2': {'copia': 117789.0703573128,
               'TART-C': 4556.428329886553,
               '3S18': 3693.6493813458133,
               'springer': 21908.8527579612,
               'accord': 7035.285939905317}}
    )


@pytest.fixture
def default_image(default_dataframe):
    return default_dataframe.plot(kind='scatter', x=0, y=1)


@pytest.fixture
def deseq_data():
    test_dict = {
        'Base mean': {'pogo': 1371.0707794911698, '3S18': 6805.37966990792},
        'log2(FC)': {'pogo': 2.6700576260657, '3S18': 1.56885380897257},
        'StdErr': {'pogo': 0.116369929972696, '3S18': 0.0880744126306213},
        'Wald-Stats': {'pogo': 22.9445667509827, '3S18': 17.8128217051217},
        'P-value': {'pogo': 1.6695197438258398e-116, '3S18': 5.620361643851719e-71},
        'P-adj': {'pogo': 7.820593691560068e-115, '3S18': 1.4189588357984098e-69}
    }
    return pd.DataFrame.from_dict(test_dict)
