Solving Raven's Progressive Matrices With Semantic Networks
===========================================================

# Introduction

We will explore the design of an AI agent capable of solving Raven's Progressive Matrices. This agent will use Semantic Networks for knowledge representation.

# Knowledge Representation

Semantic networks are a form of knowledge representation that reduces the complexity of solving a given problem. It could be thought of as a dimensionality reduction transformation; The output of which is more informative, tractable, and efficient to solve computationally. Semantic networks accomplish this by describing the problem in a manor that is limited to the essential information required to solve the problem, but without losing any information required to easily, and fully, understand the salient details.

## Design Considerations

As an overall design goal, our semantic network representation should make it possible to describe the relationship within and between each frame of Raven's Progressive Matrices. This same descriptive model can then be applied to the target frame and each possible solution. The solution with the most similar description to that of the reference frames can be considered the best possible solution. We will review each concept in this process in the following sections.

### Labeling

As a specific form of knowledge representation, semantic networks are defined as being made up of nodes, links, and labels. Constructing a semantic network to describe a problem involves assigning application specific meaning to that vocabulary of symbols. In the case of Raven's Progressive Matrices, one mapping could be made by assigning each object in a figure to a node; relationships between objects, as well as possible object transformations between figures, can be denoted with links and distinguished with labels.

### Similarity Metric

In the event that source and target frames have multiple possible transforms, it is important to establish a method for breaking ties. This can be accomplished by setting weights for each transition link in a given semantic network, and preferring the one with the best weight.

### Correspondence

Each identified object must correspond to either an object in the target frame or have a "removed" transition link. The number of ways that objects from source to target frames can be assigned is TODO. In order to find the optimal solution (the one with the highest weighted match), we must try each combination of object assignments. The time complexity of traversing this search space can be reduced by adding heuristics for declaring a solution early. These can include perfect matches, or evaluating the generated semantic networks in order of weight and the assumed difficulty of the problem.


### Matching

After establishing a method to generate semantic networks from both sample and problem frames, we then need a method for comparing them to find a solution. We could simply search for exact matches in 


# State Generation

# State Testing

# Edge Cases
