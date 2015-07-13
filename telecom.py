#!/usr/bin/env python

# Get the data (data from XPRESS)
# units = thousands of people
pop = [2, 4, 13, 6, 9, 4, 8, 12, 10, 11, 6, 14, 9, 3, 6]
sites = [[0,1,3], [1,2,4], [3,6,7,9], [4,5,7,8], [7,8,11],
    [6,9,10,11,14], [11,12,13,14]]
# units = millions of dollars
cost = [1.8, 1.3, 4.0, 3.5, 3.8, 2.6, 2.1]
budget = 10;

from gurobipy import *

def optimize(pop, sites, cost, budget):
    numR = len(pop) # Number of regions
    numT = len(sites) # Number of sites for towers

    # Create cover matrix
    cover = {};
    for i in range(numT):
        for j in range(numR):
            if (j in sites[i]):
                cover[(i,j)] = 1
            else:
                cover[(i,j)] = 0

    m = Model()

    t = {} # Binary variables for each site
    r = {} # Binary variable for each community

    for i in range(numT):
        t[i] = m.addVar(vtype=GRB.BINARY, name="t%d" % i)

    for j in range(numR):
        r[j] = m.addVar(vtype=GRB.BINARY, name="r%d" % j)

    m.update()

    for j in range(numR):
        m.addConstr(quicksum( cover[(i,j)]*t[i] for i in range(numT) ) >= r[j])

    m.addConstr(quicksum( cost[i]*t[i] for i in range(numT) ) <= budget)

    m.setObjective(quicksum( pop[j]*r[j] for j in range(numR) ), GRB.MAXIMIZE)

    m.optimize()

    solTowers = []
    solRegions = []

    for i in t:
        solTowers.append(t[i].X)

    for j in range(numR):
        solRegions.append(r[j].X)

    return [solTowers, solRegions]

print optimize(pop, sites, cost, budget)
