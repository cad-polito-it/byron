# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################

# Copyright 2023 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

# NOTE[GX]: This file contains code that some programmer may find upsetting


import networkx as nx

from byron.tools.graph import *
from byron.global_symbols import *
from byron.classes.node import NODE_ZERO
from byron.classes.node_reference import NodeReference
from byron.classes.node_view import NodeView

if matplotlib_available:
    import matplotlib.pyplot as plt


# A rainbow color mapping using matplotlib's tableau colors
SHARP_COLORS_NUM = 7
SHARP_COLORS_PALETTE = [
    "tab:blue",  # 1f77b4
    "tab:orange",  # ff7f0e
    "tab:green",  # 2ca02c
    "tab:red",  # d62728
    "tab:purple",  # 9467bd
    #'tab:brown',  # 8c564b
    #'tab:pink',  # e377c2
    #'tab:gray',  # 7f7f7f
    "tab:olive",  # bcbd22
    "tab:cyan",  # 17becf
]


def as_forest(self, filename: str | None = None, *, zoom: int = 1.0, **kwargs) -> None:
    r"""Draw the structure tree of the individual.

    Generate a figure representing the individual using NetworkX's `multipartite_layout` [1]_
    with layers corresponding to the depth of nodes in the tree structure.

    The `figsize` argument is forwarded to pyplot's `figure`.

    If `filename` is not None, instead of displaying it, the figure is saved using pyplot's savefig [2]_.
    The format is chosen by the extension.

    Possible `kwargs`, are passed to pyplot's ``savefig``.

    Notes
    -----
        Consider using ``bbox_inches='tight'`` to trim the empty border.

    Parameters
    ----------
    figsize: tuple
        pyplot's ``figsize`` in inches
    filename: str
        name of the file (format based on extension)
    kwargs:
        optional arguments for pyplot's ``savefig``

    References
    ----------
    .. [1] https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.multipartite_layout.html
    .. [2] https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html

    """

    if filename:
        fig = self.canonic_representation._draw_forest(zoom)
        fig.savefig(filename, bbox_inches='tight', **kwargs)
        plt.close()
    else:
        self.canonic_representation._draw_forest(zoom)


def as_lgp(self, filename: str | None = None, *, zoom: int = 1.0, **kwargs) -> None:
    r"""Draw the individual as a LGP genome.

    Generate a figure representing the individual using NetworkX's `multipartite_layout` [1]_ showing only the
    macros. The representation resembles those of an individual in a Linear Genetic Programming [2]_
    framework, composed of multiple linear segments.

    The `figsize` argument is forwarded to pyplot's `figure`.

    If `filename` is not None, instead of displaying it, the figure is saved using pyplot's savefig [3]_.
    The format is chosen by the extension.

    Possible `kwargs`, are passed to pyplot's ``savefig``.

    Notes
    -----
        Consider using ``bbox_inches='tight'`` to trim the empty border.

    Parameters
    ----------
    figsize: tuple
        pyplot's ``figsize`` in inches
    filename: str
        name of the file (format based on extension)
    kwargs:
        optional arguments for pyplot's ``savefig``

    References
    ----------
    .. [1] https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.multipartite_layout.html
    .. [2] https://en.wikipedia.org/wiki/Linear_genetic_programming
    .. [3] https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html

    """

    if filename:
        fig = self.canonic_representation._draw_multipartite(zoom)
        fig.savefig(filename, bbox_inches='tight', **kwargs)
        plt.close()
    else:
        self.canonic_representation._draw_multipartite(zoom)


def _draw_forest(self, zoom) -> None:
    """Draw individual using multipartite_layout"""

    T = self.structure_tree.copy()

    for n in T:
        T.nodes[n]["depth"] = len(nx.shortest_path(T, 0, n))
    height = max(T.nodes[n]["depth"] for n in T.nodes)
    width = sum(1 for n in T if self.G.nodes[n]["_type"] == MACRO_NODE)
    fig = plt.figure(figsize=(10 + zoom * width * 0.8, zoom * height + width / 2))
    ax = fig.add_subplot()

    T.remove_node(0)
    pos = nx.multipartite_layout(T, subset_key="depth", align="horizontal")
    pos = {node: (-x, -y) for (node, (x, y)) in pos.items()}
    colors = get_node_color_dict(self.G)

    # draw structure
    nx.draw_networkx_edges(
        T, pos, style=":", edge_color="lightgray", arrowstyle="-|>,head_length=.6,head_width=0.2", ax=ax
    )
    # draw macros
    nodelist = [n for n in T if self.G.nodes[n]["_type"] == MACRO_NODE]
    nx.draw_networkx_nodes(
        T, pos, nodelist=nodelist, node_color=[colors[n] for n in nodelist], node_size=800, cmap=plt.cm.tab20, ax=ax
    )
    # draw frames
    nodelist = [n for n in self.G if self.G.nodes[n]["_type"] == FRAME_NODE]
    nx.draw_networkx_nodes(
        T,
        pos,
        nodelist=nodelist,
        node_shape="s",
        node_size=800,
        node_color=[colors[n] for n in nodelist],
        cmap=plt.cm.Pastel1,
        ax=ax,
    )
    nx.draw_networkx_labels(T, pos)

    ##############################################################################
    # Draw links
    T.remove_edges_from(tuple(T.edges))
    T.add_edges_from(
        (u, v)
        for u, v, k in self.G.edges(data="_type")
        if u != v and k == LINK and T.nodes[u]["depth"] == T.nodes[v]["depth"]
    )
    nx.draw_networkx_edges(
        T,
        pos,
        edge_color=[SHARP_COLORS_PALETTE[n % SHARP_COLORS_NUM] for n in range(T.number_of_edges())],
        connectionstyle="arc3,rad=-0.3",
        arrowstyle="-|>,head_length=1,head_width=0.6",
        ax=ax,
    )

    T.remove_edges_from(tuple(T.edges))
    T.add_edges_from(
        (u, v) for u, v, k in self.G.edges(data="_type") if k == LINK and T.nodes[u]["depth"] != T.nodes[v]["depth"]
    )
    nx.draw_networkx_edges(
        T,
        pos,
        edge_color=[SHARP_COLORS_PALETTE[n % SHARP_COLORS_NUM] for n in range(T.number_of_edges())],
        arrowstyle="-|>,head_length=1,head_width=0.6",
        ax=ax,
    )

    # plt.title(f'{self}')
    plt.box(False)

    return fig


def _draw_multipartite(self, zoom: int) -> None:
    """Draw individual using multipartite_layout"""

    T = self.structure_tree.copy()
    extra_heads = list()
    for node in list(v for _, v in T.edges(NODE_ZERO) if self.genome.nodes[v]['_selement'].FORCED_PARENT):
        if self.genome.nodes[node]['_type'] == MACRO_NODE:
            extra_heads.append(node)
        target = self.genome.nodes[node]['_selement'].FORCED_PARENT
        T.remove_edge(NODE_ZERO, node)
        parent = next(n for n, f in self.genome.nodes(data='_selement') if f.__class__ == target)
        T.add_edge(parent, node)

    G = nx.DiGraph()
    sub_graphs = list()
    for s, head in enumerate(n for _, n in T.edges(0)):
        nodes = [n for n in nx.dfs_preorder_nodes(T, head) if self.G.nodes[n]["_type"] == MACRO_NODE]
        sub_graphs.append(nodes)
        G.add_nodes_from(nodes)
        for n1, n2 in zip(nodes, nodes[1:]):
            G.add_edge(n1, n2)
        for n in nodes:
            G.nodes[n]["subset"] = s
    pos = nx.multipartite_layout(G)
    # pos = {node: (-x, y) for (node, (x, y)) in pos.items()}
    colors = get_node_color_dict(self._genome)
    nodelist = list(G.nodes)

    # figsize
    fig = plt.figure(
        # layout='constrained',
        figsize=(7 + 5 * zoom + zoom * len(sub_graphs) * 2.0, zoom * max(len(s) for s in sub_graphs) * 1.2),
    )
    ax = fig.add_subplot()

    # draw heads
    heads = [s[0] for s in sub_graphs] + extra_heads
    nx.draw_networkx_nodes(G, pos, nodelist=heads[0:1], node_size=800, node_color="gold", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=heads, node_size=600, node_color="yellow", ax=ax)
    nx.draw(
        G,
        pos,
        node_color=[colors[n] for n in nodelist],
        cmap=plt.cm.tab20,
        node_size=400,
        with_labels=True,
        edge_color="lightgray",
        style=":",
        ax=ax,
    )

    labels = dict()
    for n in [_ for _ in pos if self.genome.nodes[n]['_type'] == MACRO_NODE]:
        pos[n] = (pos[n][0], pos[n][1])
        d = NodeView(NodeReference(self.genome, n)).safe_dump
        labels[n] = '     ' + d.split('\n')[0].strip() + (' …' if '\n' in d else '')
    nx.draw_networkx_labels(G, pos, horizontalalignment='left', labels=labels)

    # draw "local" references
    G.remove_edges_from(tuple(G.edges))
    for s in sub_graphs:
        G.add_edges_from(
            (u, v)
            for u, v, k in self.G.edges(data="_type")
            if k == LINK and self.G.nodes[u]['_type'] == MACRO_NODE and u in s and v in s
        )
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color=[SHARP_COLORS_PALETTE[n % SHARP_COLORS_NUM] for n in range(G.number_of_edges())],
        width=2.0,
        alpha=0.5,
        connectionstyle="arc3,rad=-.4",
        arrowstyle="-|>,head_length=.6,head_width=0.2",
        ax=ax,
    )
    # draw "global" references
    G.remove_edges_from(tuple(G.edges))
    for s in sub_graphs:
        G.add_edges_from(
            (u, v)
            for u, v, k in self.G.edges(data="_type")
            if k == LINK and ((u in s and v not in s) or (u not in s and v in s))
        )
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color=[SHARP_COLORS_PALETTE[n % SHARP_COLORS_NUM] for n in range(G.number_of_edges())],
        width=2.0,
        alpha=0.5,
        connectionstyle="arc3,rad=-.1",
        arrowstyle="-|>,head_length=.7,head_width=0.3",
        ax=ax,
    )

    # plt.title(f'Individual: {self}')
    plt.tight_layout()

    return fig
