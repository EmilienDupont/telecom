#!/usr/bin/env python

from gurobipy import *

# Sample data
# units = thousands of people
pop = [2, 4, 13, 6, 9, 4, 8, 12, 10, 11, 6, 14, 9, 3, 6]
sites = [[0,1,3], [1,2,4], [3,6,7,9], [4,5,7,8], [7,8,11],
    [6,9,10,11,14], [11,12,13,14]]
# units = millions of dollars
cost = [1.8, 1.3, 4.0, 3.5, 3.8, 2.6, 2.1]
budget = 10;


def optimize(pop, sites, cost, budget, output=False):
    numR = len(pop) # Number of regions
    numT = len(sites) # Number of sites for towers

    m = Model()

    if not output:
        m.params.OutputFlag = 0

    t = {} # Binary variables for each site
    r = {} # Binary variable for each community

    for i in range(numT):
        t[i] = m.addVar(vtype=GRB.BINARY, name="t%d" % i)

    for j in range(numR):
        r[j] = m.addVar(vtype=GRB.BINARY, name="r%d" % j)

    m.update()

    for j in range(numR):
        m.addConstr(quicksum( t[i] for i in range(numT) if j in sites[i] ) >= r[j])

    m.addConstr(quicksum( cost[i]*t[i] for i in range(numT) ) <= budget)

    m.setObjective(quicksum( pop[j]*r[j] for j in range(numR) ), GRB.MAXIMIZE)

    m.optimize()

    selTowers = []
    selRegions = []

    for i in t:
        if t[i].X > 0.5:
            selTowers.append(i)

    for j in range(numR):
        if r[j].X > 0.5:
            selRegions.append(j)

    return [selTowers, selRegions]

def handleoptimize(jsdict):
    if 'pop' in jsdict and 'sites' in jsdict and 'cost' in jsdict and 'budget' in jsdict:
        solution = optimize(jsdict['pop'], jsdict['sites'], jsdict['cost'], jsdict['budget'])
        return {'solution': solution }


if __name__ == '__main__':
    import json
    jsdict = json.load(sys.stdin)
    jsdict = handleoptimize(jsdict)
    print 'Content-Type: application/json\n\n'
    print json.dumps(jsdict)
