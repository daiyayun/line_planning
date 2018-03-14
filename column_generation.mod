# -----------------------------------------------------
# LP relaxation of line planning model
# -----------------------------------------------------

param n >= 1, integer; # number of vertices
param l >= 1, integer; # number of lines
param B >= 0; # budget
param lowerb >= 0, integer; # lower bound of frequency
param upperb >= 0, integer; # upper bound of frequency

set V:=1..n; # set of vertices
set A within {V, V}; # set of edges(directed)
set D within {V, V}; # set of od pairs
set L:=1..l; # set of lines
set F:=lowerb..upperb; # set of frequences

param od{D}; # matrice o/d
param C{L}; # fixed cost of each line
param K{L}; # capacity of each line
param line{A, L} binary; # set of all lines
param np{D}; # number of paths for each od pair
param path{(o,d) in D, {1..np[o,d]}, A} default 0; # all the paths
param time{A} >= 0; # travelling time of each edge

var x{L, F} >= 0;
var y{(o,d) in D, {1..np[o,d]}} >= 0;

minimize travel_time: sum{(o,d) in D, j in {1..np[o,d]}, (v1, v2) in A} (y[o, d, j] * time[v1, v2] * path[o, d, j, v1, v2]);

subject to demand{(o,d) in D}: sum{j in {1..np[o,d]}} y[o, d, j] = od[o, d];
subject to capacity{(v1, v2) in A}: sum{(o,d) in D, k in {1..np[o,d]}} path[o, d, k, v1, v2]*y[o, d, k] <= sum{j in L, f in F} K[j]*line[v1, v2, j]*f*x[j, f];
subject to frequence{i in L}: sum{f in F} x[i, f] <= 1;
subject to budget: sum{i in L, f in F} C[i]*x[i, f] <= B;

param pi{D};
param mu{A} >= 0;
param eta{L} >= 0;
param delta >= 0;