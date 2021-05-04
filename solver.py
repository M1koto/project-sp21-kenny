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
    use = G.copy()
    V = len(G)
    (k, c) = get_kc(V)
    c_ret = remove_c(use, c, V)
    for i in c_ret:
    	use.remove_node(i)
    k_ret = dijkstra_remove_k(use, k, V)
    return (c_ret, k_ret)

# remove nodes by considering all graphs after removal for all nodes
def remove_c(G, c, V):
    ret = []
    nodes = list(G.nodes())
    nodes.remove(0)
    nodes.remove(V-1)
    #ret has node
    while len(ret) < c:
        temp = -1
        curr = -1
        for j in nodes:
            H = G.copy()
            H.remove_node(j)
            if nx.is_connected(H):
                score = calculate_score(G, [j], [])
                if score > curr:
                    temp = j
                    curr = score
        if len(nodes) == 0 or temp == -1:
        	return ret
        #print(temp)
        nodes.remove(temp)
        if is_valid_solution(G, ret+[temp], []):
        	ret.append(temp)
    return ret

# removes k edges from shortest path, computing shortest path each time
def dijkstra_remove_k(G, k, V):
    ret = []
    for i in range(k):
        shortest = nx.dijkstra_path(G, 0, V - 1)
        #print(shortest)
        pos = min_weight_edge(shortest, G)
        if pos != -1:
            ret.append([shortest[pos], shortest[pos + 1]])
            G.remove_edge(shortest[pos], shortest[pos + 1])
        else:
            return ret
    return ret
# return true if removing any edge in s is possible
def dijkstra_possible(G, s):
	H = G.copy()
	H.remove_edge(s[0], s[1])
	if nx.is_connected(H):
		return True
	return False
def get_kc(n):
    if n <= 30:
        return (15, 1)
    elif n <= 50:
        return (50, 3)
    else:
        return (100, 5)


# Returns maximum edge on shortest path s to t, -1 IF NOT POSSIBLE
def min_weight_edge(p, G):
    ret = -1
    curr = 1000
    for i in range(len(p) - 1):
        temp = G[p[i]][p[i+1]]['weight']
        if dijkstra_possible(G, [p[i], p[i+1]]) and temp < curr:
            curr = temp
            ret = i
    return ret


'''if __name__ == '__main__':
     assert len(sys.argv) == 2
     path = sys.argv[1]
     G = read_input_file(path)
     c, k = solve(G)
     assert is_valid_solution(G, c, k)
     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
     write_output_file(G, c, k, 'outputs/ttest.out')'''

if __name__ == '__main__':
     inputs = glob.glob('inputs/large/*')
     for input_path in inputs:
         print(input_path)
         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
         G = read_input_file(input_path)
         c, k = solve(G)
         assert is_valid_solution(G, c, k)
         distance = calculate_score(G, c, k)
         write_output_file(G, c, k, output_path)

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
