param n >= 1, integer; # number of vertices
param m >= 1, integer; # number of edges
param p >= 1, integer; # number of passenger paths
param d >= 1, integer; # number of od pairs
param l >= 1, integer; # number of lines
param B >= 0; # budget
param lowerb >= 0, integer;
param upperb >= 0, integer;

set V:=1..n; # set of vertices
set A:=1..m; # set of edges(directed)
#set Aindex within {1..m,V,V}; # index for edges
set P:=1..p; # set of all passenger paths
set D:=1..d; # set of od pairs
#set Dindex within {1..d,V,V}; # index for edges
set L:=1..l; # set of lines
set F:=lowerb..upperb; # set of frequences

param od{D}; # matrice o/d
param C{L}; # fixed cost of each line
param K{L}; # capacity of each line
param line{L, A} binary; # set of all lines
param path{P, A} binary; # set of all passenger paths
param np{D}; # number of paths for each od pair
param time{P} >= 0; # travelling time of each path

var x{L, F} binary;
var y{P} >= 0;

minimize travel_time: sum{i in P} time[i]*y[i];

param ei {i in D} := sum{j in {1..i}} np[j];
param si {i in D} := ei[i] - np[i] + 1;
subject to demand{i in D}: sum{j in {si[i]..ei[i]}} y[j] = od[i];
subject to capacity{i in A}: sum{j in P} path[j, i]*y[j] <= sum{j in L, f in F} K[j]*line[j, i]*f*x[j, f];
subject to frequence{i in L}: sum{f in F} x[i, f] <= 1;
subject to budget: sum{i in L, f in F} C[i]*x[i, f] <= B;
