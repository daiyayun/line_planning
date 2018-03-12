## Random data generation for line programming problem
import random as rand
import numpy as np

n = 100
prob = 1/n
lowerb = 1 #frequencies parameters
upperb = 4
budget = 10
linenumb = 4
timelimit = 10

print('Generating random graph')

## Generating random graph
m = 0 # number of edges
edges = [] # List of edges
edgeNumber = {} # Index of each edge
adjMat = np.zeros( (n,n) ) #Adjacency matrix
neighbors = {} # List of neighbors
for i in range(1,n+1):
    neighbors[i] = []
    for j in range(1,n+1):
        if (i!=j and rand.random() <= prob):
            m+=1
            edges.append( (i,j) )
            edgeNumber[(i,j)] = m
            adjMat[i-1,j-1] = 1
            neighbors[i].append(j)
            
# print('Edges:\n')
# for i in range(len(edges)):
#     print(edges[i])

print('Generating OD matrix')

## Generating OD Matrix
d = 0 # Number of OD pairs
dlim = 5 #upper limit for OD values
odprob = 0.75 #Probability of an OD pair
od = []
for i in range(n):
    for j in range(n):
        if (i!=j and rand.random() <= odprob):
            d+=1
            od.append( (i+1,j+1,round(rand.uniform(0,dlim),2) ))
            
# print('\nOD pairs:\n')
# for i in range(1,n+1):
#     print('%s: %s %s' % (i, od[i][0], od[i][1]))
    
print('Generating lines')
            
## Generating lines
lines = np.zeros( (linenumb, m), dtype=int )
stopprob = 1-(1/n) # Probability of stopping the transportation line at one given step of the generation
triesAllowed = 3 # Number of tries allowed when encountering a cycle during the line generation
for i in range(linenumb):
    start = rand.randint(1,n)
    current = start
    line = [start]
    stop = False
    tries = 0
    while (not stop):
        if (rand.random() >= stopprob):
            stop = True
        else:
            neighborList = neighbors[current]
            if (not neighborList): # Test if next is empty
                stop=True
            else:
                next = neighborList[rand.randint(0,len(neighborList)-1)]
                if (next in line): 
                    if (tries >= triesAllowed):
                        stop=True
                    else:
                        tries+=1
                else:
                    line.append(next)
                    current = next
                    tries = 0
    for step in range(len(line) - 1):
        lines[i,edgeNumber[(line[step], line[step+1])]-1] = 1
        
## Generating time values for arcs and paths
arctimes = [rand.uniform(0,timelimit) for i in range(m)]
        
print('Generating paths')
        
## Generate Paths
def paths(graph, v):
    """Generate the maximal cycle-free paths in graph starting at v.
    graph must be a mapping from vertices to collections of
    neighbouring vertices.
    """
    
    path = [v]                  # path traversed so far
    seen = {v}                  # set of vertices in path
    def search():
        dead_end = True
        for neighbour in graph[path[-1]]:
            if neighbour not in seen:
                dead_end = False
                seen.add(neighbour)
                path.append(neighbour)
                yield from search()
                path.pop()
                seen.remove(neighbour)
        if dead_end:
            yield list(path)
    yield from search()

p = 0 # Number of paths
allpaths = {}
odpaths = []
nbpaths = []
pathtimes = []
for i in range(1, n+1):
    for j in range(1,n+1):
        if (i!=j):
            allpaths[(i,j)] = []
    pathfromi = sorted(paths(neighbors, i))
    for path in pathfromi:
        if path[-1] != i:
            allpaths[i, path[-1]].append(path)
for i in range(d):
    nb = len(allpaths[(od[i][0], od[i][1])])
    nbpaths.append(nb)
    p+=nb
    for path in allpaths[(od[i][0], od[i][1])]:
        duration = 0
        binarypath = [0 for i in range(m)]
        for j in range(len(path)-1):
            binarypath[edgeNumber[(path[j],path[j+1])]-1] = 1
            duration += arctimes[edgeNumber[(path[j],path[j+1])]-1]
        odpaths.append(binarypath)
        pathtimes.append(round(duration,2))
        
        
## Write in file
with open('line_plan_r.dat', 'w') as file:
    
    ## Parameters
    file.write('param n := %s;\n' % n)
    file.write('param d := %s;\n' % d)
    file.write('param p := %s;\n' % p)
    file.write('param l := %s;\n' % linenumb)
    file.write('param B := %s;\n' % budget)
    file.write('param m := %s;\n' % m)
    file.write('param lowerb := %s;\n' % lowerb)
    file.write('param upperb := %s;\n\n' % upperb)
    
    ## Edges index
    file.write('set Aindex :=\n')
    for i in range(m):
        file.write('%s %s %s    ' % (i+1, edges[i][0], edges[i][1]))
        if (i%10 == 9):
            file.write('\n')
    file.write(';\n\n')
    
    ## OD matrix and index
    file.write('param od :=\n')
    for i in range(d):
        file.write('%s %s    ' % (i+1, od[i][2]))
        if (i%10 == 9):
            file.write('\n')
    file.write(';\n\n')
    
    file.write('set Dindex :=\n')
    for i in range(d):
        file.write('%s %s %s   ' % (i+1, od[i][0], od[i][1]))
        if (i%10 == 9):
            file.write('\n')
    file.write(';\n\n')
    
    ## Costs (constant = 1)
    file.write('param C :=\n')
    for i in range(linenumb):
        file.write('%s 1   ' % (i+1))
        if (i%10 == 9):
            file.write('\n')
    file.write(';\n\n')
    
    ## Capacities (constant = 1)
    file.write('param K :=\n')
    for i in range(linenumb):
        file.write('%s 1   ' % (i+1))
        if (i%10 == 9):
            file.write('\n')
    file.write(';\n\n')
    
    ## Lines
    file.write('param line: ')
    for i in range(1, m+1):
        file.write('%s ' % i)
    file.write(':=\n')
    for i in range(linenumb):
        file.write('%s    ' % (i+1))
        for j in range(m):
            file.write('%s ' % lines[i,j])
        file.write('\n')
    file.write(';\n\n')
    
    ## Paths, number of paths and time
    file.write('param path: ')
    for i in range(1, m+1):
        file.write('%s ' % i)
    file.write(':=\n')
    for i in range(p):
        file.write('%s    ' % (i+1))
        for j in range(m):
            file.write('%s ' % odpaths[i][j])
        file.write('\n')
    file.write(';\n\n')
    
    file.write('param np:=\n')
    for i in range(d):
        file.write('%s %s   ' % (i+1, nbpaths[i]))
        if (i%10 == 9):
            file.write('\n')
    file.write(';\n\n')
    
    file.write('param time:=\n')
    for i in range(p):
        file.write('%s %s   ' % (i+1, pathtimes[i]))
        if (i%10 == 9):
            file.write('\n')
    file.write(';\n\n')
    
print('Done')