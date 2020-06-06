# NEAT-Flappy-Bird
AI that learns to play the Flappy Bird Game using NEAT (NeuroEvolution of Augmenting Topologies).

# Introduction
This classical flappy bird uses genetic algorithm to learn to play the game. It learns to play the game by just calculating  the distance of bird from the top pipe and the distance of bird from the bottom pipe then produces the output whether to jump or not based on the neural network.

# Description
The genetic algorithm produces 100 birds and then check which bird perform best according to the fitness value and then select the best bird pass their features to next generation and do the same thing for that until the algorithm achieve the desire result.
It uses hyperbolic tan function as activation function which squash the value between -1 and 1. Then jump according to that whether the 
output is greater than 0.5 or not. And fitness_criterion is set to max so remove that birds which does not perform well. And other setting 
can find on https://neat-python.readthedocs.io/en/latest/ here.
