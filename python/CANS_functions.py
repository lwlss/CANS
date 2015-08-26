from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import random


def convertij(pos, NCol):
    '''Converts row i, col j into row-major vector index'''
    i = pos[0]
    j = pos[1]
    return((i-1)*NCol+(j-1))


def convertind(ind, NCol):
    '''Converts row-major vector index into row i and col j'''
    row = ind//NCol
    col = ind-row*NCol
    return((row+1, col+1))


def neighbours(pos, NRow, NCol):
    '''Returns valid list of neighbours for cell at row i, col j'''
    i = pos[0]
    j = pos[1]
    candidates = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
    return([coords for coords in candidates if 1 <= coords[0] and
            1 <= coords[1] and coords[0] <= NRow and coords[1] <= NCol])


def distance(posA, posB):
    '''Returns the Euclidean distance between two coordinates'''
    return(np.sqrt((posA[0] - posB[0])**2 + (posA[1] - posB[1]) ** 2))


#print(neighbours((2,2),3,3))
#print(neighbours((1,1),3,3))
#print(convertij((2,2),2))
#print(convertind(9,3))


def makeModelCANS(nrow, ncol, rparams, rA, rC, rS, kN, kS):
    '''Set up variables and return a function suitable for simulating CANS dynamics with scipy.odeint'''
    # Convert between indices and coordinates generate neighbourhoods and calculate distances
    inds = [x for x in range(0, nrow * ncol)]
    coords = [convertind(i, nrow) for i in inds]
    neighbcoords = [neighbours(coord, nrow, ncol) for coord in coords]
    neighbinds = [[convertij(neighb, nrow) for neighb in neighblist] for neighblist in neighbcoords]
    dists = [[distance(coord, neighb) for neighb in neighbs] for coord, neighbs in zip(coords, neighbcoords)]

    # Indices to convert from long vector to species-specific vectors
    Cinds = inds
    Ainds = [ind + len(inds) for ind in inds]
    Ninds = [ind + 2 * len(inds) for ind in inds]
    Sinds = [ind + 3 * len(inds) for ind in inds]
    
    def f(y, t):
        '''Calculates rate of change of variables for CANS model given current value of variables (and time t)'''
        # Cannot have negative cell numbers or concentrations
        y = np.maximum(0, y)
        Cvals = y[Cinds]
        Avals = y[Ainds]
        Nvals = y[Ninds]
        Svals = y[Sinds]
        dC = [r * C * N - rA * C * S + rC * A for r, C, N, S, A in zip(rparams, Cvals, Nvals, Svals, Avals)]
        dA = [rA * C * S - rC * A for C, S, A in zip(Cvals, Svals, Avals)]
        dN = [-r * C * N - kN * sum([N - Nvals[neighbind] for neighbind in neighbs]) for r, C, N, neighbs, ndists in zip(rparams, Cvals, Nvals, neighbinds, dists)]
        dS = [rS * C - kS * sum([S-Svals[neighbind] for neighbind in neighbs]) for C, S, neighbs, ndists in zip(Cvals, Nvals, neighbinds, dists)]
        return(dC + dA + dN + dS)
    return(f)


def makeModelComp(nrow, ncol, rparams, k):
    '''Set up variables and return a function suitable for simulating competition model dynamics with scipy.odeint'''
    # Convert between indices and coordinates generate neighbourhoods and calculate distances
    inds = range(0, nrow * ncol)
    coords = [convertind(i, ncol) for i in inds]
    neighbcoords = [neighbours(coord, nrow, ncol) for coord in coords]
    neighbinds = [[convertij(neighb, nrow) for neighb in neighblist] for neighblist in neighbcoords]

    # Indices to convert from long vector to species-specific vectors
    Cinds = inds
    Ninds = [ind + len(inds) for ind in inds]

    def f(y, t):
        '''Calculates rate of change of variables for competition model given current value of variables (and time t)'''
        # Cannot have negative cell numbers or concentrations
        y = np.maximum(0, y)
        Cvals = y[Cinds]
        Nvals = y[Ninds]
        dC = [r * C * N for r, C, N in zip(rparams, Cvals, Nvals)]
        dN = [-r * C * N - k * sum([N - Nvals[neighbind] for neighbind in neighbs]) for r, C, N, neighbs in zip(rparams, Cvals, Nvals, neighbinds)]
        return(dC + dN)
    return(f)


