% Utilizing Generate and Test, Means-Ends, and Problem Reduction in Designing an AI Agent to Solve Raven's Progressive Matrices
% Magahet Mendiola
  (mmendiola3@mail.gatech.edu)
% January 18th, 2015


## Introduction

We will explore the concepts of Problem Reduction, Means-Ends Analysis, and Generate and Test in the context of solving RPMs.


## Problem reduction

The concept of problem reduction is that a complex problems can be subdivided into multiple, simpler, problems. Humans do this quite naturally. For example, when preparing a meal, we do not expect to go directly from a pantry of raw ingredients to a Thanksgiving feast. We break down the overall goal into the set of dishes to be served. Each dish is then further divided into the phases of preparation and cooking required for each. Although thousands of individual actions may be required overall, we are able to easily, and naturally, de-construct the problem into very simple and rote tasks.

In the case of developing AI agents to solve RPMs, problem reduction again provides a way to simplify the very complex overall goal. The task of solving RPMs could be decomposed the following way:

- Generate valid semantic networks for frames A and B.
    - Label objects in frame A
    - Create semantic network nodes and links showing spatial relationships between objects.
    - Label objects in frame B in each possible way
    - Complete the semantic network showing the transform links for each possible combination of transforms given the corresponding object labels.
    - Yield or store the generated semantic network for evaluation.
 
- Find the transformations that describe the relationship between C the answer choices.
    - Taking each generated semantic network representing the relationship between A and B, apply that transform to C.
    - Match the resulting figure X to each of the answer choices.
    - If a match is found, store the result along with the semantic network.

- Find the best weighted semantic network among those that describe the relationship between C and the answer choices.
    - Compute the sum of the weights of each valid semantic network.
    - Return the answer choice with the best sum of weights.

By breaking down the complex task of finding a solution to an RPM, the separate problems that remain are simple enough to handle with naive processes. This methodical approach to problem solving also simplifies the conceptualization of the solution. This makes the task of engineering an AI agent simply a matter of coding modular components to perform each of these sub-goals; then to design interfaces between each component to hand off the current state of the solution to the next modular component.


## Generate and Test

Generate and Test is a methodology for problem solving which involves the creation of possible solutions and the evaluation of these to test their viability as the correct answer. This process requires two components. The first is the solution generator, which creates possible solutions based on an application specific set of rules. The second component is the tester, which compares each generated solution against application specific criteria in order to determine whether a given answer is correct.

We can utilize Generate and Test all throughout the design of our RPM agent. From the previous breakdown of our agent's tasks, we notice that the first main process is to generate valid semantic networks to describe the relationship between A and B. We can think of this sub-task as a generator of transformation descriptions. These descriptions are then tested, in the second main sub-task, against the figures in C and each of the answer choices.

Generate and Tes

## Means-Ends Analysis

Means-Ends Analysis is a concept which says that solutions can be found incrementally, by taking small steps and evaluating whether you have moved closer to the final goal. There are many examples of this methodology, including A* path-finding and hill-climbing optimization. A* uses a heuristic that evaluates whether a given movement (the means), would bring us closer to the goal position (the ends). As the algorithm runs, it searches the landscape for the most direct path to the goal. Hill-climbing, likewise, takes incremental steps in the feature space and performs an evaluation of whether the change had a positive or negative effect. Means-Ends is a powerful methodology in solving complex problems incrementally. It can be thought of as a method of problem reduction in that it reduces a complex problem, like finding a safe path through rough terrain, into a simpler problem of finding how to reach a very nearby point that happens to be incrementally closer to the final goal.

In our RPM problem solving, Means-Ends Analysis can be used in a number of ways. First, 



