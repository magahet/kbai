#!/usr/bin/env python


import argparse
import os
import collections
import itertools
from Agent import Agent
from VisualProblemSet import VisualProblemSet


def main(problemSet, problems, root='Problems (Image Data)'):
    sets = []

    for file in os.listdir(root):
        if problemSet and problemSet not in file:
            continue
        newSet = VisualProblemSet(file)
        sets.append(newSet)
        for num, problem in enumerate(sorted(os.listdir(root + os.sep + file))):
            if problems and num + 1 not in problems:
                continue
            newSet.addProblem(file, problem)

    agent = Agent()
    correct = collections.defaultdict(int)

    ids_3x3 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

    ids_3x3 = (
        'ACG',
        'BCH',
        'DFG',
        'EFH',
        'AGC',
        'DGF',
        'BHC',
        'EHF',
    )

    ids_2x2 = (
        'ABC',
        'ACB',
    )
    available_voters = agent.available_voters.keys()
    for num in range(1, len(available_voters) + 1):
        print num
        for voters in itertools.combinations(available_voters, num):
            print voters,
            for set in sets:
                for problem in set.getProblems():
                    if problem.getProblemType() != '2x1 (Image)':
                        continue
                    if agent.solve2x1_train(problem, voters) == problem.correctAnswer:
                        correct[voters] += 1
            print correct[voters]

    #for frames in itertools.permutations(ids_3x3, 3):
        #print frames
        #for set in sets:
            #for problem in set.getProblems():
                #if problem.getProblemType() != '3x3 (Image)':
                    #continue
                #if agent.solve3x3_train(problem, frames) == problem.correctAnswer:
                    #correct[frames] += 1

    ordered = sorted(correct.items(), key=lambda x: x[1])
    print ordered

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--set', '-s')
    parser.add_argument('--problems', '-p', type=int, nargs=argparse.REMAINDER)
    args = parser.parse_args()
    main(args.set, args.problems)
