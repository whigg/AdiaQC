'''

File: tetris_hebbrule.py
Author: Hadayat Seddiqi
Date: 4.5.13
Description: Recognize tetris pieces with a quantum Hopfield network
             using the Hebbian learning rule.

'''

import scipy as sp

nQubits = 4
#T = 10.0
T = sp.arange(0.1,20,0.1) # Output a sequence of anneal times
dt = 0.01*T

# Output parameters
output = 1 # Turn on/off all output except final probabilities
eigspecdat = 0 # Output data for eigspec
eigspecplot = 0 # Plot eigspec
eigspecnum = 2**nQubits # Number of eigenvalues
fidelplot = 1 # Plot fidelity
fideldat = 1 # Output fidelity data
fidelnumstates = 2**nQubits # Check fidelity with this number of eigenstates
overlapdat = 0 # Output overlap data
overlapplot = 0 # Plot overlap
outputdir = 'data/hopfield/tetris/n4p' # In relation to run.py
probout = 0 # Calculate final state probabilities
mingap = 0 # Output minimum spectral gap
outdat = 1 # Output probabilities and mingap

errchk = 0 # Error-checking on/off
eps = 0.01 # Numerical error in normalization condition (1 - norm < eps)

# Specify a QUBO (convert to Ising = True), or alpha, beta directly 
# (convert = False), and also specify the signs on the Ising Hamiltonian 
# terms (you can specify coefficients too for some problems if needed)
isingConvert = 0
isingSigns = {'hx': -1, 'hz': -1, 'hzz': -1}

neurons = nQubits
memories = [ [ 1,-1, 1,-1],
             [-1, 1,-1, 1],
             [ 1, 1,-1,-1],
             [-1,-1, 1, 1],
             [ 1,-1,-1, 1],
             [-1, 1, 1,-1] ]

inputstate = [1, 1, -1, 1]

# This is gamma, the appropriate weighting on the input vector
isingSigns['hz'] *= 1 - (len(inputstate) - inputstate.count(0))/(2*neurons)

alpha = sp.array(inputstate)
beta = sp.zeros((neurons,neurons))
delta = sp.array([])

# Construct pattern matrix
for i in range(neurons):
    for j in range(neurons):
        for p in range(len(memories)):
            beta[i,j] += ( memories[p][i]*memories[p][j] -
                           len(memories)*(i == j) )

beta = sp.triu(beta)/float(neurons)
print beta