# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

"""Tests for the ``clusters: all`` path of ``cluster_network``."""

import pypsa

from scripts.cluster_network import busmap_for_all_buses, clustering_for_n_clusters


def make_network():
    n = pypsa.Network()
    # OSM-style bus names that do not start with the country code
    n.add("Bus", "relation/1", v_nom=380, x=0, y=0, country="DE", carrier="AC")
    n.add("Bus", "way/2", v_nom=380, x=1, y=0, country="DE", carrier="AC")
    n.add("Bus", "relation/3", v_nom=380, x=2, y=0, country="FR", carrier="AC")
    n.add("Line", "l1", bus0="relation/1", bus1="way/2", x=0.1, r=0.01, s_nom=100, v_nom=380, build_year=0)
    n.add("Line", "l2", bus0="way/2", bus1="relation/3", x=0.1, r=0.01, s_nom=100, v_nom=380, build_year=0)
    return n


def test_busmap_for_all_buses_has_country_prefix():
    n = make_network()
    busmap = busmap_for_all_buses(n)
    assert (busmap.str[:2] == n.buses.country.reindex(busmap.index)).all()
    assert busmap.is_unique
    assert busmap.index.equals(n.buses.index)


def test_all_buses_clustering_renames_buses():
    n = make_network()
    busmap = busmap_for_all_buses(n)
    nc = clustering_for_n_clusters(n, busmap).n
    assert len(nc.buses) == len(n.buses)
    assert len(nc.lines) == len(n.lines)
    assert (nc.buses.index.str[:2] == nc.buses.country).all()
