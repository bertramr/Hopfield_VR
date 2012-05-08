%% main.m
%
%% HopfieldNetwork

h = Hopfield(200);
P = 5;
ratio = 0.5;
mu = 1;
flip_ratio = 0.2;
h.run(P, ratio, mu, flip_ratio);