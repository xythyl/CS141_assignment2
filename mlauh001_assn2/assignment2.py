#    Matthew Lauhakamin
#    860989596
#    mlauh001@ucr.edu

import sys
import re
import time

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    pathPairs=[]
    # [((s,t),w)]
    d = {}
    p = {}
    for source in G[0]:
        for node in G[0]:
            d[node] = float('inf')
            p[node] = None
        if source >= len(G[0]):
            return
        d[source] = 0
        for i in range(len(G[0])-1):
            for u in G[0]:
                for v in range(len(G[1])):
                    if d[v] > d[u] + G[1][u][v]:
                        d[v] = d[u] + G[1][u][v]
                        p[v] = u
        for u in G[0]:
            for v in range(len(G[1])):
                if d[v] > d[u] + G[1][u][v]:
                    print ("Negative edge detected in Bellman-Ford!")
                    return
        for i in range(len(d)):
            pathPairs.append(((source,i),d[i]))
    print("Bellman-Ford Pairs: \n" + str(pathPairs) + "\n")
    return pathPairs

def FloydWarshall(G):
    pathPairs=[]
    # [((s,t),w)]
    m = G[1]
    d = {}
    p = {}
    for source in G[0]:
        for node in G[0]:
            d[node] = float('inf')
            p[node] = None
        if source >= len(G[0]):
            return
        d[source] = 0
        for k in range(len(G[0])):
            for u in range(len(G[0])):
                for v in range(len(G[0])):
                    m[u][v] = G[1][u][v]
                    if d[v] > d[u] + G[1][u][v]:
                        d[v] = d[u] + G[1][u][v]
                        p[v] = u
                    if m[u][v] > m[u][k] + m[k][v]:
                        m[u][v] = m[u][k] + m[k][v]
        for u in G[0]:
            for v in range(len(G[1])):
                if d[v] > d[u] + G[1][u][v]:
                    print ("Negative edge detected in Floyd-Warshall!")
                    return
        for i in range(len(d)):
            pathPairs.append(((source,i),d[i]))
    print("Floyd-Warshall Pairs: \n" + str(pathPairs) + "\n")
    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=int(edgeMatch.group(3)) # bugfix: converted str to int
            edges[int(source)-1][int(sink)-1]=weight
    #Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)

def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        FloydWarshall(G)
    if algorithm == "both":
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        start=time.clock() # bugfix: swapped line 73 and line 74
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment2.py -<f|b> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print('python assignment2.py -<f|b> <input_file>')
        quit(1)
    main(sys.argv[2],sys.argv[1])
