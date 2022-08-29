# -*- coding: utf-8 -*-
"""FinalClustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15bMAU3FrXFr_VCSgXfo5U7ao_RJnJq1o
"""

!pip install dimod dwave-system

import networkx as nx
import numpy as np
from dimod import DiscreteQuadraticModel
from dwave.system import LeapHybridDQMSampler
from dwave.cloud import Client
from numpy import genfromtxt


def modularization(G, B, num_partitions):
  partitions = range(num_partitions)
  # Initialize the DQM object
  dqm = DiscreteQuadraticModel()

  for i in G.nodes():
      dqm.add_variable(num_partitions, label=i)

  for i in G.nodes():
      for j in G.nodes():
          if i==j:
              continue #the algorithm skips the linear term in QUBO/Ising formulation as in k-community a node has to belong to one community, therefore there is no effect in the maximising constellation
          dqm.set_quadratic(i,j, {(c, c): ((-1)*B[i,j]) for c in partitions})


  # Initialize the DQM solver
  sampler = LeapHybridDQMSampler(token='DEV-b1e20d4b8484c8c21e6bd035a200465a1a59e82e')
  # sampler = greedy.SteepestDescentSampler()
  #sampleset = sampler.sample(dqm)

  # Solve the problem using the DQM solver
  sampleset = sampler.sample_dqm(dqm)

  # get the first solution
  sample = sampleset.first.sample
  energy = sampleset.first.energy

  run_time=(sampleset.info['run_time'])*0.001 #total runtime in milliseconds

  # Count the nodes in each partition
  counts = np.zeros(num_partitions)
      
  #create communities as parameter for evaluation function
  communities=[]
  for k in partitions:
      comm=[]
      for i in sample:
          if sample[i]==k:
              comm.append(i)
      communities.append(set(comm))

  #compute number of nodes in each community
  for i in sample:
      counts[sample[i]] += 1
  
  return (communities, run_time, energy, counts,sample)


A = genfromtxt('Edge_AAL90_Binary.csv', delimiter='	')
G = nx.from_numpy_matrix(A)
B=nx.modularity_matrix(G)
num_partitions=16


result = modularization(G,B,num_partitions) #a former version has been used with additional parameters B,k; basic algorithm the same as in later evaluation
#mod=nx.algorithms.community.quality.modularity (G, result[0])
#print(mod, result[1])

import networkx.algorithms.community as nx_comm
nx_comm.modularity(G, nx_comm.label_propagation_communities(G))

num_partitions

color_map = []
colors = {0: 'blue', 1: 'red', 2: 'green', 3: '#cce6ff', 4:'pink', 5: 'green', 6: 'brown', 7:'yellow', 8: '#0059b3', 9: 'red', 10: 'green', 11: 'black', 12:'pink', 13: 'green', 14: '#1aff1a', 15: 'brown', 16: 'gray'}
for node in G:
    color_map.append(colors[result[4][node]])
   
nx.draw(G, node_color=color_map, with_labels=True)

clus = np.zeros((len(G), 2))

for i, node in enumerate(G):
  clus[i, 0] = node
  clus[i, 1] = result[4][node]

np.savetxt("clustering.csv", clus, delimiter=",")