import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    k, c = get_kc(len(G))
    c_ret = remove_c(G)
    k_ret = dijkstra_remove_k(G)
    return c_ret, k_ret
def remove_c(G):
	ret = []
	for i in range(c):
		temp = 0
		curr = 0
		for j in G.node():
			H = G.copy()
	    	H.remove_node(j)
			if nx.is_connected(H):
				score = calculate_score(G, [j], [])
				if score > curr:
					temp = j
					curr = score
		G.remove_node(temp)
		ret.append(temp)
	return ret
				
def dijkstra_remove_k(G):
	ret = []
	for i in range(k):
    	shortest = nx.dijkstra_path(G, 0, len(G) - 1)
    	removed = False
    	while removed is False:
    		dame = []
    		pos = max_weight_edge(shortest, G, dame)
	    	H = G.copy()
	    	H.remove_edge(shortest[pos], shortest[pos+1])
	    	if nx.is_connected(H):
	    		ret.append([shortest[pos], shortest[pos+1]])
	    		G.remove_edge(shortest[pos], shortest[pos+1])
	    		removed = True
	    	else:
	    		dame = [pos]
	return ret

def get_kc(G):
	if len(G) <= 30:
		return 15, 1
	else if len(G) <= 50:
		return 50, 3
	else:
		return 100, 5

def max_weight_edge(p, G, no):
	ret = 0
	curr = 0
	if len(no) != 0:
		p = p[:no[0]]
	for i in range(len(p) - 1):
		temp = G[p[i]][p[i]+1]['weight']
		if temp > curr:
			curr = temp
			ret = i
	return ret

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
