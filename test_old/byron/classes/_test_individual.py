# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

# from byron.global_symbols import FRAMEWORK, NODE_ZERO
# from byron.classes.readymade_macros import MacroZero
# from byron.classes.fitness import FitnessABC
# from byron.classes.frame import FrameABC
# from byron.ea.graph import *
# import pytest
# from unittest.mock import Mock
# from byron.classes.individual import Individual
# import networkx as nx

# # def test_individual_creation():
# #     G = nx.MultiDiGraph()

# #     G.add_node(1)
# #     G.add_node(2)
# #     G.add_node(3)

# #     G.add_edge(1, 2)
# #     G.add_edge(2, 3)
# #     G.add_edge(3, 1)

# #     ind1 = Individual(top_frame=G)
# #     ind2 = Individual(top_frame=G)

# #     assert ind1.fitness == None
# #     assert ind2.fitness == None
# #     ind1.fitness = 42
# #     ind2.fitness = 43
# #     assert ind1.fitness == 42
# #     assert ind2.fitness == 43
# #     ind2.fitness = 42
# #     assert ind1.fitness == ind2.fitness
# #     assert ind1.genome != ind2.genome
# #     my_dict = {}

# #     G = nx.MultiDiGraph()
# #     G.add_nodes_from(range(100, 110))
# #     ind1 = Individual(top_frame=G)
# #     ind2 = Individual(top_frame=G)

# #     assert ind1.fitness == None
# #     assert ind2.fitness == None

# #     my_dict = {}

# import pytest
# import networkx as nx
# from byron.classes import Individual
# import byron as byron

# def test_individual_properties():
#     G = nx.MultiDiGraph()
#     G.add_nodes_from(range(100, 110))
#     ind1 = Individual(top_frame=G)

# def test_individual_fitness_setter():
#     G = nx.MultiDiGraph()
#     G.add_nodes_from(range(100, 110))
#     ind1 = Individual(top_frame=G)
#     ind1.fitness = 42
#     assert ind1.fitness == 42

# def test_individual_str():
#     G = nx.MultiDiGraph()
#     G.add_nodes_from(range(100, 110))
#     ind1 = Individual(top_frame=G)

# def unit_test():
#     macro1a = byron.f.macro('1')
#     macro1b = byron.f.macro('call {m1}', m1=byron.f.global_reference('frame1'))
#     frame1 = byron.f.bunch([macro1a, macro1a, macro1a, macro1a, macro1b], name='frame1', size=10_000)
#     frame2 = byron.f.bunch([macro1a], name='frame2', size=10_000)
#     new_individual = byron.classes.Individual(top_frame=frame1)
#     new_individual.G.add_edge(8, 29, key='test', kind='link')
#     new_individual.G.add_edge(20, 26, key='test', kind='link')

# def test_individual_properties():
#     macro1a = byron.f.macro('1')
#     macro1b = byron.f.macro('call {m1}', m1=byron.f.global_reference('frame1'))
#     frame1 = byron.f.bunch([macro1a, macro1a, macro1a, macro1a, macro1b], name='frame1', size=10_000)
#     frame2 = byron.f.bunch([macro1a], name='frame2', size=10_000)
#     individual = Individual(top_frame=frame1)
#     individual.G.add_edge(8, 29, key='test', kind='link')
#     individual.G.add_edge(20, 26, key='test', kind='link')

#     unroll(individual, frame2)

#     assert individual.grammar_tree == nx.DiGraph()
#     assert individual.G == individual.genome
#     assert individual.fitness == None

# def test_individual_fitness_setter():
#     top_frame = MockFrame()
#     individual = Individual(top_frame)

#     mock_fitness = MockFitness(100)
#     individual.fitness = mock_fitness

#     assert individual.fitness == mock_fitness

# def test_individual_equality():
#     top_frame1 = MockFrame()
#     individual1 = Individual(top_frame1)

#     top_frame2 = MockFrame()
#     individual2 = Individual(top_frame2)

#     assert individual1 == individual2

# def test_individual_inequality():
#     top_frame1 = MockFrame()
#     individual1 = Individual(top_frame1)

#     top_frame2 = MockFrame()
#     individual2 = Individual(top_frame2)

#     mock_fitness = MockFitness(100)
#     individual2.fitness = mock_fitness

#     assert individual1 != individual2

# def test_individual_str():
#     top_frame = MockFrame()
#     individual = Individual(top_frame)

#     assert "Individual with" in str(individual)
#     assert "n_nodes" in str(individual)
#     assert "n_macros" in str(individual)
#     assert "n_frames" in str(individual)
#     assert "n_links" in str(individual)
#     assert "n_params" in str(individual)
