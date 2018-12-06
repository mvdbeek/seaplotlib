"""Create UMAP plots from a directory of DamID deseq data."""

import os
from functools import reduce

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap

sns.set(style='white', context='notebook', rc={'figure.figsize': (14, 10)})
DIR = 'deseq2 datasets/'
LOG2_COLUMN = 2


def plot_umap(embedding, data, protein, fig, ax, alpha=0.03, cmap='RdYlBu_r'):
    """Dispatch to plotting log2 intensity over 2D representation or histogram of clustered GATC density"""
    if not protein:
        plot_density_umap(embedding, ax, fig)
    else:
        plot_chrom_umap(embedding, data, protein, fig, ax, alpha=alpha, cmap=cmap)


def plot_chrom_umap(embedding, data, protein, fig=None, ax=None, alpha=0.03, cmap='RdYlBu_r'):
    """Plot UMAP visulatization."""
    if fig is None:
        fig, ax = plt.subplots()
    mappable = ax.scatter(embedding[:, 0], embedding[:, 1], alpha=alpha, c=data[protein], cmap=cmap)
    plot_colorbar(mappable, fig, ax)
    ax.set_title(protein)
    return ax


def plot_density_umap(embedding, ax, fig, alpha=0.03, cmap='RdYlBu_r', title='GATC density'):
    """Plot GATC density."""
    mappable = ax.hist2d(embedding[:, 0], embedding[:, 1], bins=[100, 100], cmap=cmap, normed=True)[-1]
    plot_colorbar(mappable, fig, ax)
    ax.set_title(title)


def plot_colorbar(mappable, fig, ax):
    """Plot colorbar"""
    cbar = fig.colorbar(mappable, ax=ax)
    cbar.set_alpha(1)
    cbar.draw_all()


def read_data_from_direcotry(path):
    datasets = [os.path.join(DIR, d) for d in os.listdir(DIR)]
    dataframes = [
        pd.read_csv(d, sep='\t', header=None, names=['index', os.path.basename(d)[len('DESeq2 '):-len('.tabular')]],
                    index_col=0, usecols=[0, LOG2_COLUMN]) for d in datasets]
    df_final = reduce(lambda left, right: pd.merge(left, right, on='index'), dataframes)
    return df_final


def fit_transform(df):
    reducer = umap.UMAP()
    embedding = reducer.fit_transform(df)
    return reducer, embedding


def load_embedding(path):
    return np.array(pd.read_csv(path, sep='\t'))


def save_embedding(embedding, path):
    pd.DataFrame.from_records(embedding).to_csv(path, sep='\t')


def plot_proteins(embedding, df):
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(20, 15))
    for ax, protein in zip(axes.flat, reversed(list(df.columns) + [None])):
        plot_umap(embedding=embedding, data=df, protein=protein, ax=ax, fig=fig)
    fig.tight_layout()
    return fig
