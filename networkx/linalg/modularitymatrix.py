"""Modularity matrix of graphs.
"""
#    Copyright (C) 2004-2017 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
from __future__ import division
import networkx as nx
from networkx.utils import not_implemented_for
__author__ = "\n".join(['Aric Hagberg <aric.hagberg@gmail.com>',
                        'Pieter Swart (swart@lanl.gov)',
                        'Dan Schult (dschult@colgate.edu)',
                        'Jean-Gabriel Young (Jean.gabriel.young@gmail.com)'])
__all__ = ['modularity_matrix', 'directed_modularity_matrix']


@not_implemented_for('directed')
@not_implemented_for('multigraph')
def modularity_matrix(G, nodelist=None, weight=None):
    """Return the modularity matrix of G.

    The modularity matrix is the matrix B = A - <A>, where A is the adjacency
    matrix and <A> is the average adjacency matrix, assuming that the graph
    is described by the configuration model.

    More specifically, the element B_ij of B is defined as
        A_ij - k_i k_j / 2 * m
    where k_i(in) is the degree of node i, and were m is the number of edges
    in the graph. When weight is set to a name of an attribute edge, Aij, k_i, 
    k_j and m are computed using its value. 

    Parameters
    ----------
    G : Graph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().
    
    weight : string or None, optional (default=None)
       The edge attribute that holds the numerical value used for
       the edge weight.  If None then all edge weights are 1.

    Returns
    -------
    B : Numpy matrix
      The modularity matrix of G.

    Examples
    --------
    >>> import networkx as nx
    >>> k =[3, 2, 2, 1, 0]
    >>> G = nx.havel_hakimi_graph(k)
    >>> B = nx.modularity_matrix(G)


    See Also
    --------
    to_numpy_matrix
    adjacency_matrix
    laplacian_matrix
    directed_modularity_matrix

    References
    ----------
    .. [1] M. E. J. Newman, "Modularity and community structure in networks",
       Proc. Natl. Acad. Sci. USA, vol. 103, pp. 8577-8582, 2006.
    """
    if nodelist is None:
        nodelist = list(G)
    A = nx.to_scipy_sparse_matrix(G, nodelist=nodelist, weight=weight,
                                  format='csr')
    k = A.sum(axis=1)
    m = k.sum() * 0.5
    # Expected adjacency matrix
    X = k * k.transpose() / (2 * m)
    return A - X


@not_implemented_for('undirected')
@not_implemented_for('multigraph')
def directed_modularity_matrix(G, nodelist=None, weight=None):
    """Return the directed modularity matrix of G.

    The modularity matrix is the matrix B = A - <A>, where A is the adjacency
    matrix and <A> is the expected adjacency matrix, assuming that the graph
    is described by the configuration model.

    More specifically, the element B_ij of B is defined as
        B_ij = A_ij - k_i(out) k_j(in) / m
    where k_i(in) is the in degree of node i, and k_j(out) is the out degree
    of node j, with m the number of edges in the graph. When weight is set
    to a name of an attribute edge, Aij, k_i, k_j and m are computed using
    its value.

    Parameters
    ----------
    G : DiGraph
       A NetworkX DiGraph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default=None)
       The edge attribute that holds the numerical value used for
       the edge weight.  If None then all edge weights are 1.

    Returns
    -------
    B : Numpy matrix
      The modularity matrix of G.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.DiGraph()
    >>> G.add_edges_from(((1,2), (1,3), (3,1), (3,2), (3,5), (4,5), (4,6),
    ...                   (5,4), (5,6), (6,4)))
    >>> B = nx.directed_modularity_matrix(G)


    Notes
    -----
    NetworkX defines the element A_ij of the adjacency matrix as 1 if there
    is a link going from node i to node j. Leicht and Newman use the opposite
    definition. This explains the different expression for B_ij.

    See Also
    --------
    to_numpy_matrix
    adjacency_matrix
    laplacian_matrix
    modularity_matrix

    References
    ----------
    .. [1] E. A. Leicht, M. E. J. Newman, 
       "Community structure in directed networks",
        Phys. Rev Lett., vol. 100, no. 11, p. 118703, 2008.
    """
    if nodelist is None:
        nodelist = list(G)
    A = nx.to_scipy_sparse_matrix(G, nodelist=nodelist, weight=weight,
                                  format='csr')
    k_in = A.sum(axis=0)
    k_out = A.sum(axis=1)
    m = k_in.sum()
    # Expected adjacency matrix
    X = k_out * k_in / m
    return A - X


# fixture for nose tests
def setup_module(module):
    from nose import SkipTest
    try:
        import numpy
        import scipy
    except:
        raise SkipTest("NumPy not available")
