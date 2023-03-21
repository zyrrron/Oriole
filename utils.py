# Load required modules
import csv
# import random
# import matplotlib.pyplot as plt
# from matplotlib import cm
# import matplotlib
import networkx as nx
# import metis
# from collections import Counter
import numpy as np
import time
import argparse
import copy
# import numpy.linalg as la
# import scipy.cluster.vq as vq
# import itertools
# import operator
# import math
# import collections
# from mpmath import *
# from itertools import chain
# from itertools import product
# from itertools import starmap
# from functools import partial
# import os
# import seaborn as sns
# import shutil
# from networkx.drawing.nx_agraph import graphviz_layout
# import re
# import ujson
# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
# import numpy.linalg as la
# import scipy.cluster.vq as vq
# import scipy
from pycallgraph2.output import GraphvizOutput

##########################################
### create file names                  ###
##########################################

def edgelist_filename (settings, sample):
	return settings[sample]['graph_path']+'/DAG.edgelist'


##########################################
### load files                         ###
##########################################

def load_settings (filename):
	"""Load the settings file"""
	settings = {}
	data_reader = csv.reader(open(filename, 'rU'), delimiter='\t')
	# Ignore header
	header = next(data_reader)
	# Process each line
	for row in data_reader:
		if len(row) == len(header):
			sample = row[0]
			sample_data = {}
			for el_idx, el in enumerate(header[1:]):
				sample_data[el] = row[el_idx+1]
			settings[sample] = sample_data
	return settings


def load_graph (settings, sample):
	"""
	read DAG edgelist, return DIRECTED graph, and input/output nodes
	"""
	G = nx.read_edgelist (edgelist_filename (settings, sample), nodetype = str, create_using=nx.DiGraph())
	return G

def load_graph_undirected (settings, sample):
	"""
	read DAG edgelist, return UNDIRECTED graph, and input/output nodes
	"""
	G = nx.Graph()
	G = nx.read_edgelist (edgelist_filename (settings, sample), nodetype=str)
	return G

def load_metis_part_sol (inputfile):
	"""
	read metis partition result
	"""
	lines = [open(inputfile, 'r').read().strip("\n")][0].split('\n')
	cut = int( lines[0].split('\t')[1] )
	partDict = {}
	for line in lines[1:]:
		tokens = line.split('\t')
		part = int( tokens[0].split(' ')[-1] )
		nodes = tokens[1].split(',')
		partDict[part] = nodes
	# print(partDict)
	return cut, partDict

def get_nonprimitive_nodes (G):
	"""
	Obtain nonprimitive nodes of a DAG
	input nodes (in_nodes) - in_degree is 0
	output nodes (out_nodes) - out_degree is 0
	"""
	in_nodes, out_nodes = [], []
	for node in G.nodes():
		indegree = G.in_degree(node)
		outdegree = G.out_degree(node)
		if outdegree == 0:
			out_nodes.append(node)
		if indegree == 0:
			in_nodes.append(node)
	nonprimitives = in_nodes + out_nodes
	return in_nodes, out_nodes, nonprimitives

def get_G_primitive (G, nonprimitives):
	"""
	if primitive only is True, remove input and output nodes
	"""
	G_primitive = nx.DiGraph()
	for edge in G.edges():
		if edge[0] not in nonprimitives and edge[1] not in nonprimitives:
			G_primitive.add_edge(*edge)
	return G_primitive


def loadSettings():
	# Parse the command line inputs
	parser = argparse.ArgumentParser(description="perform graph partition using metis")
	parser.add_argument("-settings", dest="settings", required=True, help="settings.txt", metavar="string")
	parser.add_argument("-samples", dest="samples", required=True, help="1,2", metavar="string")
	args = parser.parse_args()

	# Run the command
	samples = args.samples.split(',')
	settings = load_settings(args.settings)
	return samples, settings


def loadData(s, settings):

	print('Processing sample', s)
	# print (settings[s])
	# obtain user-defined params
	tmp = settings[s]['S_bounds'].split(',')
	S_bounds = [eval(i) for i in tmp]
	target_n = settings[s]['target_n'].split(',')
	primitive_only = settings[s]['primitive_only']
	ConstraintType = settings[s]['high_low_flag'].split(',')[0]
	constraint = []
	if ConstraintType.lower() == 'high':
		tmp = settings[s]['high_constraint'].split(',')
		for i in tmp:
			constraint.append(eval(i))
	else:
		constraint.append(int(settings[s]['low_constraint'].split(',')[0]))
	loop_free = False
	if settings[s]['loop_free'].lower == 'true':
		loop_free = True
	priority = settings[s]['priority']
	trajectories = int(settings[s]['trajectories'])
	out_path = settings[s]['output_path']
	timestep = 10000000000
	begin_time_current_step = time.time()

	# load graph
	G = load_graph_undirected(settings, s)
	DAG = load_graph(settings, s)

	in_nodes, out_nodes, nonprimitives = get_nonprimitive_nodes(DAG)

	if primitive_only == 'TRUE':
		G_primitive = get_G_primitive(DAG, nonprimitives)
	else:
		G_primitive = copy.deepcopy(DAG)

	return G_primitive, S_bounds, primitive_only, ConstraintType, constraint, loop_free, priority, out_path, timestep