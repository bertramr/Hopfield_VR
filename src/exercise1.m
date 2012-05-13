%% Exercise 1
%
%% Exercise 1.1
% Implement the Hopfield network as described above.
% Shortly comment on your implementation.
% The overlap of the network in state S(t) with a given pattern 
% ... is defined by ...
% Set N = 200, P = 5, c = .2. For the first two unit time steps of the
% retrieval of one pattern, plot the changing values of the energy function
% and the overlap of the network with the pattern as the
% state of each node is sequentially updated

h = Hopfield(200);
P = 5;
ratio = 0.5;
mu = 1;
flip_ratio = 0.2;
h = h.run(P, ratio, mu, flip_ratio, true);

gcf;
print('../tex/img/exer1_1m.png','-dpng');
close;

%% Exercise 1.2
%
% Using the overlap defined in 1.1, derive an expression for the 
% percentage of pixels in the network state S which differ from the 
% pattern mu . This is the (normalized) pixel distance.

% See Hopfield.m: get.pixelDistance

%% Exercise 1.3
% We define the retrieval error of a pattern mu in a Hopfield network as
% the normalized pixel distance of the network state S to the pattern mu 
% after convergence, when retrieving the pattern mu as described above.
% Set N = 200 and c = 0.1. Plot the mean retrieval error of a randomly 
% chosen pattern averaged over different network realizations as a function
% of the dictionary size P . Average over enough network realizations to 
% give a smooth curve and give error bars for the estimation of the mean
% (you can assume the variation to be normally distributed). From your 
% data points and the chosen confidence interval, roughly estimate a maximal
% P at which patterns can be retrieved from the network with a 
% mean retrieval error of less than 2%?

N = 200;
h = Hopfield(N);
flip_ratio = 0.1;
ratio = 0.5;

P = 50;
Q = 100;

mu = 1;
error = zeros(Q,P);
for p = 1:P
    for q = 1:Q
        mu = randi(p,1);
        h = h.run(p, ratio, mu, flip_ratio, false);
        error(q,p) = h.meanRetrievalError(mu);
    end
end
e = std(error);
y = mean(error);

boxplot(error,'plotstyle','compact')
title(sprintf('Mean retrieval error (N=%d, Q=%d)',N,Q));
ylabel('mean retrieval error');
xlabel('# patterns');
grid on
print(sprintf('../tex/img/exer1_3m-box_error_N%d_Q%d.png',N,Q),'-dpng');
close;

errorbar(y,e);
title(sprintf('Mean retrieval error (N=%d, Q=%d)',N,Q));
ylabel('mean retrieval error');
xlabel('# patterns');
grid on
hold on
plot([1 50],[0.02 0.02],'--r');
print(sprintf('../tex/img/exer1_3m-bar_error_N%d_Q%d.png',N,Q),'-dpng');
close;


