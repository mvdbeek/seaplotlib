"""Create UMAP plots from a directory of DamID deseq data."""

import collections
import os
import math
from functools import reduce

import hdbscan
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap

sns.set(style='white', context='notebook', rc={'figure.figsize': (14, 10)})
DIR = 'deseq2 datasets/'
LOG2_COLUMN = 2

_Result = collections.namedtuple('ClusteringResult', 'embedding clusterable_embedding labels')

class Result(object):

    def __init__(self, embedding=None, clusterable_embedding=None, labels=None, figure=None):
        self.embedding = embedding
        self.clusterable_embedding = clusterable_embedding
        self.labels = labels
        self.figure = figure


def plot_umap(embedding,
              data,
              protein,
              fig,
              ax,
              result,
              alpha=0.03,
              cmap='RdYlBu_r',
              vmin=None,
              vmax=None,
              clip=False,
              auto_color_scale=True,
              **kwargs):
    """Dispatch to plotting log2 intensity over 2D representation or histogram of clustered GATC density"""
    if protein == 'density':
        plot_density_umap(embedding, fig=fig, ax=ax)
    elif protein == 'cluster':
        plot_cluster(embedding, data, fig=fig, ax=ax, result=result)
    else:
        if auto_color_scale:
            vmin = data.min().min()
            vmax = data.max().max()
        plot_chrom_umap(embedding,
                        data,
                        protein,
                        fig=fig,
                        ax=ax,
                        alpha=alpha,
                        cmap=cmap,
                        vmin=vmin,
                        vmax=vmax,
                        clip=clip,
                        **kwargs)
    label_cluster(result=result, ax=ax)
    return result


def plot_cluster(embedding, data, fig, ax, result):
    result.clusterable_embedding = create_clusterable_embedding(df=data)
    result.labels = hdbscan.HDBSCAN(
        min_samples=10,
        min_cluster_size=2500,
    ).fit_predict(result.clusterable_embedding)
    clustered = (result.labels >= 0)
    ax.scatter(embedding[~clustered, 0],
                embedding[~clustered, 1],
                c=(0.5, 0.5, 0.5),
                s=0.1,
                alpha=0.5)
    mappable = ax.scatter(embedding[clustered, 0],
                embedding[clustered, 1],
                c=result.labels[clustered],
                s=0.1,
                cmap='Spectral')

    plot_colorbar(mappable, fig, ax)


def label_cluster(result, ax):
    if result.labels is not None:
        s = pd.Series(result.labels)
        for label in s.unique():
            ax.annotate(str(label),
                         (result.embedding[s == label][:, 0].mean(),
                          result.embedding[s == label][:, 1].mean()),
                         horizontalalignment='center',
                         verticalalignment='center',
                         weight='bold',
                         color='black',
                         )


def plot_chrom_umap(embedding,
                    data,
                    protein,
                    fig=None,
                    ax=None,
                    alpha=0.03,
                    cmap='RdYlBu_r',
                    vmin=None,
                    vmax=None,
                    clip=False,
                    **kwargs):
    """Plot UMAP visulatization."""
    if fig is None:
        fig, ax = plt.subplots()
    cmap = matplotlib.cm.get_cmap(cmap)
    normalize = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=clip)
    mappable = ax.scatter(embedding[:, 0], embedding[:, 1], s=0.1, c=data[protein], cmap=cmap, norm=normalize)
    plot_colorbar(mappable, fig, ax)
    ax.set_title(protein)
    return ax


def plot_density_umap(embedding, fig, ax, alpha=0.03, cmap='RdYlBu_r', title='GATC density'):
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
    datasets = [os.path.join(path, d) for d in os.listdir(path)]
    dataframes = [
        pd.read_csv(d, sep='\t', header=None, names=['index', os.path.basename(d)[len('DESeq2 '):-len('.tabular')]],
                    index_col=0, usecols=[0, LOG2_COLUMN]) for d in datasets]
    df_final = reduce(lambda left, right: pd.merge(left, right, on='index'), dataframes)
    return df_final

def create_clusterable_embedding(df, n_neighbors=30, min_dist=0.0, n_components=2, random_state=42, metric='canberra', **kwargs):
    return umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        random_state=random_state,
        metric=metric,
        **kwargs
    ).fit_transform(df)


def fit_transform(df, random_state=42, **kwargs):
    reducer = umap.UMAP(random_state=random_state, **kwargs)
    embedding = reducer.fit_transform(df)
    return reducer, embedding


def load_embedding(path):
    return np.array(pd.read_csv(path, sep='\t'))


def save_embedding(embedding, path):
    pd.DataFrame.from_records(embedding).to_csv(path, sep='\t', index=None)


def plot_proteins(embedding, df, density=True, cluster=False, clip=False, **kwargs):
    elements = list(df.columns)
    if density:
        elements.append('density')
    if cluster:
        elements.append('cluster')
    nrows = int(math.ceil(len(elements) / 2.0))
    fig, axes = plt.subplots(ncols=2, nrows=nrows, figsize=(20, 15))
    result = Result(embedding=embedding, figure=fig)
    for ax, protein in zip(axes.flat, reversed(elements)):
        result = plot_umap(embedding=embedding, data=df, protein=protein, ax=ax, fig=fig, result=result, clip=clip, **kwargs)
    fig.tight_layout()
    return result
