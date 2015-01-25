% Utilizing Generate and Test, Means-Ends, and Problem Reduction in Designing an AI Agent to Solve Raven's Progressive Matrices
% Magahet Mendiola
  (mmendiola3@mail.gatech.edu)
% January 18th, 2015


## Introduction

We will explore the concepts of Problem reduction, Means-Ends, and Generate and Test in the context of solving RPMs.


## Problem reduction

The concept of problem reduction is that a complex problem can be subdivided into multiple, simpler, problems. We do this all the time in everyday life. For example,

The task of solving RPMs can be decomposed into the following:

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

By breaking down the complex task of finding a solution to an RPM, the seperate problems that remain are simple enough to handle with naive processes. This methodical approach to problem solving also simplifies the conceptualization of the solution. This makes the task of engineering an AI agent simply a matter of coding modular componants to perform each of these sub-goals; then to design interfaces between each componant to hand off the current state of the solution to the next modular componant.


## Generate and Test

Generate and Test is a methodology for solving problems which involves two constructs. The first is the solution generator. This componant creates possible solutions based on an application specific set of rules. The second componant is the tester.

## Means-Ends

When evaluating
