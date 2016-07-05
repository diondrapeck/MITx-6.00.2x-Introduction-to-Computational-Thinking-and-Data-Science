# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from problemset5_graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23

    Returns:
        a directed graph representing the map
    """
    
    print "Loading map from file..."
    
    mapFile = open(mapFilename)
    campus = WeightedDigraph()

    for line in mapFile:
        start, end, dist, outDist = line.split()
        node1, node2 = Node(start), Node(end)
        for node in [node1, node2]:
            try:
                campus.addNode(node)
            except ValueError, newEdge:
                continue
        newEdge = WeightedEdge(node1, node2, float(dist), float(outDist))
        campus.addEdge(newEdge)
    return campus
        
mitMap = load_map("C:/Users/diond\Documents/Python/mitx-6.00.2x-introduction-to-computational-thinking-and-data/ps5_mit_map.txt")

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """

    start = Node(start)
    end = Node(end)
    
    assert start, end in digraph.nodes
    
    # Depth-first search through digraph
    def DFS(start, maxTotalDist, maxDistOutdoors, best = None, path = []):
        
        path = path + [start]
        
        if start == end:
            if maxTotalDist >= 0 and maxDistOutdoors >= 0:
                return path
                
        for node in digraph.childrenOf(start):
            if node not in path: #avoid cycles due to repeated nodes
                if not best or len(path) < len(best):
                    dist = float(digraph.edges[start][0][1][0])
                    outdoorDist = float(digraph.edges[start][0][1][1])
                    newTotDist = maxTotalDist - dist
                    newOutDist = maxDistOutdoors - outdoorDist
                    if newOutDist < 0:
                        continue
                    newPath = DFS(node, newTotDist, newOutDist, best, path)
                    if newPath:
                        best = newPath
        return best

    shortest_path = DFS(start, maxTotalDist, maxDistOutdoors)
    
    if shortest_path:
        return [str(node) for node in shortest_path]
    else:
        raise ValueError
        




# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
#     Test cases
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges


    LARGE_DIST = 1000000

#     Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "Correct? BFS: {0}".format(expectedPath1 == brutePath1)


#     Test case 2
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "Correct? BFS: {0}".format(expectedPath3 == brutePath3)

