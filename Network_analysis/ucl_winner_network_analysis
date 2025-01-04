import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('ucl-finals.csv')

# Create a directed graph
G = nx.DiGraph()
winners = []
weights = {}
# Add edges from loser to winner
for _, row in df.iterrows():
    winner = row['winner']
    runner_up = row['runner-up']
    if winner not in weights:
        weights[winner] = 1
    else:
        weights[winner] += 1
    # Add weighted edge from runner-up to winner
    G.add_edges_from([(runner_up, winner)])
pos = nx.spring_layout(G, k=.6, iterations= 25)
nx.draw_networkx(G,pos, with_labels= True)
plt.show()


sorted_weight = sorted(weights.items(), key=lambda x:x[1], reverse=True)

print('Team Weights')
print()
for key, value in sorted_weight:
    print(f'team: {key}  wins: {value}')

print('')

degree_centrality=nx.degree_centrality(G)

print('Degree of Centrality')
print('')    
i = 1
sorted_degree_centrality = sorted(degree_centrality.items(), key=lambda x:x[1], reverse=True)
for team, centrality in sorted_degree_centrality[:20]:
   print(f'{i}. {team} {centrality}')
   i += 1

print()

print('Eigenvector Centrality')
print()
eigenvector_centrality=nx.eigenvector_centrality(G)

i= 1
sorted_ev_centrality = sorted(eigenvector_centrality.items(), key=lambda x:x[1], reverse=True)
for team, centrality in sorted_ev_centrality[:20]:
    print(f'{i}. {team} {centrality}')
    i += 1
