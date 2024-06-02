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
# import ujson
# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
# import numpy.linalg as la
# import scipy.cluster.vq as vq
# import scipy
import re
# from pycallgraph2.output import GraphvizOutput


##########################################
### create file names                  ###
##########################################

def edgelist_filename (settings, sample):
	return settings[sample]['graph_path']+'/DAG.edgelist'


##########################################
### load files                         ###
##########################################

def read_json(inputfile):
	lines = [open(inputfile, 'r').read().strip("\n")][0].split('\n')
	ports, gates = {}, {}
	for idx, line in enumerate(lines):
		line = line.strip()
		if line.startswith('"ports"'):
			p_s = idx
			searchlines = lines[idx+1:]
			for i, sl in enumerate(searchlines, idx):
				if sl.strip().startswith('"cells"'):
					p_e = i+1
		if line.startswith('"cells"'):
			g_s = idx
			searchlines = lines[idx+1:]
			for i, sl in enumerate(searchlines, idx):
				if sl.strip().startswith('"netnames"'):
					g_e = i

	# get information of inputs and outputs
	spacer = [idx + p_s + 1 for idx, line in enumerate(lines[p_s + 1:p_e]) if ': {' in line.strip()]
	for i, v in enumerate(spacer):
		# get names
		s = lines[v].strip()
		s = re.search('"(.*)"', s)
		el = s.group(1)
		ports[el] = {}
		# get directions
		s = lines[v + 1].strip()
		s = re.search('"direction": "(.*)"', s)
		direction = s.group(1)
		ports[el]['direction'] = direction
		# get offset if it exists
		s = lines[v + 2].strip()
		if s[-1] == ',':
			offset = s.split(':')[1].split(',')[0].strip()
			ports[el]['offset'] = int(offset)
			s = lines[v + 3].strip()
		# get bits
		bits = s.split('[')[1].split(']')[0].strip()
		if ',' in bits:
			del ports[el]
			continue
		else:
			if bits == '"0"':
				ports[el]['bits'] = 0
			else:
				ports[el]['bits'] = int(bits)
	# get information of gates
	spacer = [idx+g_s+1 for idx, line in enumerate(lines[g_s+1:g_e]) if '$abc$' in line.strip()]
	for i, v in enumerate(spacer):
		# get names
		s = int(lines[v].strip().split('"')[1].split('$')[-1])
		gates[s] = {}
		gates[s]['input'] = {}
		gates[s]['output'] = {}
		# search for attributes of this gate
		if i != len(spacer)-1:
			searchlines = lines[v:spacer[i+1]]
		else:
			searchlines = lines[v:]
		for sl in searchlines:
			# get gate type
			if sl.strip().startswith('"type"'):
				gatetype = re.search('_(.*)_', sl.strip())
				if not gatetype:
					continue
				gates[s]['type'] = gatetype.group(1)
			# get input(s)
			if sl.strip().startswith('"A": [') or sl.strip().startswith('"B": [') or sl.strip().startswith('"C": [') or sl.strip().startswith('"D": [') \
					or sl.strip().startswith('"S": ['):
				port = re.search('"(.*)"', sl).group(1)
				bits = sl.split('[')[1].split(']')[0].strip()
				gates[s]['input'][port] = int(bits)
			# get output
			# stop loop after getting output edge ID
			if sl.strip().startswith('"Y": ['):
				port = re.search('"(.*)"', sl).group(1)
				bits = sl.split('[')[1].split(']')[0].strip()
				gates[s]['output'][port] = int(bits)
			if sl.strip().startswith('"$auto$'):
				break
	return ports, gates


def synthesize_graph(ports, gates, outdir, t):
	G = nx.DiGraph()
	# start from the output, add edges
	edges = []
	for p in ports:
		if ports[p]['direction'] == 'output':
			b = ports[p]['bits']
			for g in gates:
				if b == gates[g]['output']['Y']:
					edges.append((g, p))

	for p in ports:
		if ports[p]['direction'] == 'input':
			b = ports[p]['bits']
			for g in gates:
				if b == gates[g]['input']['A']:
					edges.append((p, g))

				if gates[g]['type'] != 'NOT':
					if b == gates[g]['input']['B']:
						edges.append((p, g))
				if gates[g]['type'] in ['MUX', 'NMUX']:
					if b == gates[g]['input']['S']:
						edges.append((p, g))
				if gates[g]['type'] in ['AOI3', 'OAI3', 'AOI4', 'OAI4']:
					if b == gates[g]['input']['C']:
						edges.append((p, g))
				if gates[g]['type'] in ['AOI4', 'OAI4']:
					if b == gates[g]['input']['D']:
						edges.append((p, g))


	for g in gates:
		op = gates[g]['output']['Y']
		for sg in gates:

			# Ron update on 09/05/2023, add more gate types inside
			if gates[sg]['type'] == 'NOT':
				gin = [gates[sg]['input']['A']]
			elif gates[sg]['type'] in ['MUX', 'NMUX']:
				gin = [gates[sg]['input']['A'], gates[sg]['input']['B'], gates[sg]['input']['S']]
			elif gates[sg]['type'] in ['AOI3', 'OAI3']:
				gin = [gates[sg]['input']['A'], gates[sg]['input']['B'], gates[sg]['input']['C']]
			elif gates[sg]['type'] in ['AOI4', 'OAI4']:
				gin = [gates[sg]['input']['A'], gates[sg]['input']['B'], gates[sg]['input']['C'], gates[sg]['input']['D']]
			else:
				gin = [gates[sg]['input']['A'], gates[sg]['input']['B']]
			if op in gin:
				edges.append((g, sg))

	for e in edges:
		G.add_edge(*e)

	nx.write_edgelist(G, outdir+'/DAG.edgelist')


# generate port-gate dictionary.
def generateGateDict(data, outpath):
	csv_file = f'{outpath}/port_gate.csv'

	with open(csv_file, 'w', newline='') as file:
		writer = csv.writer(file)

		writer.writerow(['key', 'input', 'output', 'type'])

		for key, value in data.items():
			input_data = value['input']
			output_data = value['output']
			row = [key, value['type'], input_data, output_data]
			writer.writerow(row)


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
	target_n = int(settings[s]['target_n'].split(',')[0])
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
	if settings[s]['loop_free'].lower() == 'true':
		loop_free = True
	bio_flag = int(settings[s]['ColorFlag'])
	out_path = settings[s]['output_path']

	# "attempts" means the number of possible merging paths we will collect, note that each path includes multiple partition results
	# time step for verification stage
	# time step for merging stage
	# height: searching depth for each community merging propaganda checking
	# "height2": the depth of searching possible merging solution for un-neighbor communities in every propaganda checking
	# Upper bound for continuously negative reward path in each propaganda checking
	attempt_range = []
	tmp = settings[s]['attempt_range'].split(',')
	for i in tmp:
		attempt_range.append(eval(i))
	timestep = int(settings[s]['timestep_v'])
	timestep2 = int(settings[s]['timestep_m'])
	height = int(settings[s]['height'])
	height2 = int(settings[s]['height2'])
	ub = int(settings[s]['ub'])

	# parameters for edge coloring.
	# Assume we have at most n different cell-cell communication molecular for one benchmark,
	# set n as the element in the below color list: "color_upperbounds".
	# SingleFlag = True: Only check one solution file
	# SingleFlag = False: Check a list of potential solution
	color_upperbound = int(settings[s]['color_upperbound'])
	trace_back = int(settings[s]['timestep_traceback'])
	check_interval = int(settings[s]['check_interval'])
	SingleFlag = True
	if settings[s]['SingleFlag'] == '1':
		SingleFlag = False

	# load graph
	# G = load_graph_undirected(settings, s)
	DAG = load_graph(settings, s)

	in_nodes, out_nodes, nonprimitives = get_nonprimitive_nodes(DAG)

	if primitive_only == 'TRUE':
		G_primitive = get_G_primitive(DAG, nonprimitives)
	else:
		G_primitive = copy.deepcopy(DAG)

	return G_primitive, S_bounds, target_n, primitive_only, ConstraintType, constraint, loop_free, out_path, timestep, timestep2, \
		bio_flag, height, DAG, height2, attempt_range, ub, color_upperbound, trace_back, check_interval, SingleFlag
