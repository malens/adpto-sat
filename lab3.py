import copy
import decimal
import math
import os
import random
import pycosat
import dimacs


def satexperiment(n):
    S = [1, -1]
    results = {}

    V = range(1, n + 1)
    for a in range(1 * n, 10 * n, 1):
        results[a] = 0
        for t in range(0, 100):
            formula = []
            for i in range(0, a):
                clause = []
                for k in range(0, 3):
                    var = random.choice(V) * random.choice(S)
                    clause.append(var)
                formula.append(clause)
            solution = pycosat.solve(formula)
            if solution != u'UNSAT':
                results[a] += 1
        results[a] /= 100
    return results


def prepareedgeclause(i, j, k):
    clause = [[-((i - 1) * k + x), -((j - 1) * k + x)] for x in range(1, k + 1)]
    return clause


def preparevertexclause(i, k):
    clause = [[j + (i - 1) * k for j in range(1, k + 1)]]
    # print(clause)
    for j in range((i - 1) * k + 1, i * k + 1):
        for p in range(j + 1, i * k + 1):
            clause += [[-j, -p]]
    # print(clause)
    return clause


def checkcolouring(solution, edgelist, k):
    coloring = {(x - 1) // k + 1: x % k + 1 for x in solution if x > 0}
    print(coloring)
    for (i, j) in edgelist:
        if coloring[i] == coloring[j]:
            return False
    return True


preparevertexclause(1, 5)


def graphcoloringtosat(graph, k):
    edgeList = dimacs.edgeList(graph)
    satclause = []
    vertexclauses = []
    for i, j in edgeList:
        if i not in vertexclauses:
            satclause += preparevertexclause(i, k)
            vertexclauses += [i]
        if j not in vertexclauses:
            satclause += preparevertexclause(j, k)
            vertexclauses += [j]
        satclause += prepareedgeclause(i, j, k)
    return satclause


def printresults():
    for key, value in satexperiment(10).items():
        print(key, " ", value)

def solveone(colnum, filename):
    graph = dimacs.loadGraph("all-instaces/" + filename)
    edgelist = dimacs.edgeList(graph)
    sat = graphcoloringtosat(graph, colnum)
    # print(sat)
    sol = pycosat.solve(sat)

    # print("\n", sol)
    if sol != u'UNSAT':
        print(checkcolouring(sol, edgelist, colnum))

def solveall():
    directory = os.fsencode("all-instaces")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".col"):
            print(filename)
            graph = dimacs.loadGraph("all-instaces/" + filename)
            edgelist = dimacs.edgeList(graph)
            g = copy.deepcopy(graph)
            k = 2
            sol = pycosat.solve(graphcoloringtosat(g, k))
            while sol == u'UNSAT' and k < 1000:
                print(k)
                k += 1
                g = copy.deepcopy(graph)
                sol = pycosat.solve(graphcoloringtosat(g, k))

            print(filename, k, checkcolouring(sol, edgelist, k))

# for k in range (3, 20):
#     solveone(k, "1-FullIns_3.col")

solveall()