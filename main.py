from clustering import modularization, COLORS 
import networkx as nx
import numpy as np 
from numpy import genfromtxt
import csv
import time
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm

def main(folder, data_name):
    A = genfromtxt(f'data/{data_name}.csv', delimiter='	')
    G = nx.from_numpy_matrix(A)
    B = nx.modularity_matrix(G)
    
    # Report network specs:
    """
    print("Clsutering Coefficient: ", nx.average_clustering(G))
    print("Average degree:", np.array(G.degree()).mean(axis=0)[-1])
    degree = np.array([i for i in nx.degree_centrality(G).values()])
    print("Average degree centrality: ", degree.mean())
    """
    for k in [4]:
        mods_LCDA, times_LCDA, Ncomms = [], [], []
        for r in range(100):
            #communities, run_time, energy, counts, sample = modularization(G, B, k) #a former version has been used with additional parameters B,k; basic algorithm the same as in later evaluation

            start = time.time()
            communities_class = nx_comm.louvain_communities(G)#, seed=123)
            
            end = time.time()
            total_time = end - start
            mods_LCDA.append(nx_comm.modularity(G, communities_class))
            times_LCDA .append(total_time)
            Ncomms.append(len(communities_class))

            '''
            headers = ['modularity_classical', 'modularity_quantum', 'communities', 'run_time_dwave', 'energy', 'counts', 'sample', 'communities_class_louvain', 'time_louvain']
            data = [nx_comm.modularity(G, communities_class),  nx_comm.modularity(G, communities), communities, run_time, energy, counts, sample, communities_class, total_time]
            with open(f'{folder}/{data_name}run{k}_{r}.csv', 'w') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerow(data)
            file.close()

            color_map = []

            for node in G:
                color_map.append(COLORS[sample[node]])
            f = plt.figure()

            nx.draw(G, node_color=color_map, with_labels=True, ax=f.add_subplot(111))
            f.savefig(f"{folder}/{data_name}graph{k}_{r}.png")

            clus = np.zeros((len(G.nodes), 2))

            for i, node in enumerate(G):
                clus[i, 0] = node
                clus[i, 1] = sample[node]

            np.savetxt(f"{folder}/{data_name}clustering{k}_{r}.csv", clus, delimiter=",")
            '''
        mods_LCDA, times_LCDA, Ncomms = np.array(mods_LCDA), np.array(times_LCDA), np.array(Ncomms)
        print(f"In k={k} LCDA results are as follow: ")
        print(f"Mean modularity of {mods_LCDA.mean()} with a standard deviation of {mods_LCDA.std()}")
        print(f"LCDA took and average time of {times_LCDA.mean()} seconds")
        print(f"The mean number of communities is {Ncomms.mean()}")
    
if __name__ == '__main__':
    main(folder='output', data_name='Edge_AAL90_Binary')