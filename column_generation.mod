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
param path{i in D, {1..np[i]}, A}; # all the paths
param time{A} >= 0; # travelling time of each edge

var x{L, F} >= 0;
var y{i in D, {1..np[i]}} >= 0;

minimize travel_time: sum{i in D, j in {1..np[i]}, a in A} (y[i, j] * time[a] * path[i, j, a]);

subject to demand{i in D}: sum{j in {1..np[i]}} y[i, j] = od[i];
subject to capacity{i in A}: sum{j in D, k in {1..np[j]}} path[j, k, i]*y[j, k] <= sum{j in L, f in F} K[j]*line[i, j]*f*x[j, f];
subject to frequence{i in L}: sum{f in F} x[i, f] <= 1;
subject to budget: sum{i in L, f in F} C[i]*x[i, f] <= B;

param pi{D};
param mu{A} >= 0;
param eta{L} >= 0;
param delta >= 0;