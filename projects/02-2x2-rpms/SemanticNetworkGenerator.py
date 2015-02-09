from CorrespondenceGenerator import CorrespondenceGeneratorWithAddRemove
from SemanticNetwork import SemanticNetwork


class SemanticNetworkGenerator(object):
    '''A generator of semantic networks for RPMs.'''

    def __init__(self, problem):
        '''Initialize the generator from a provided RPM'''
        self.problem = problem

    def __iter__(self):
        figureA = self.problem.figures.get('A')
        figureB = self.problem.figures.get('B')
        for objectMap in self.iterObjectAssignment(figureA, figureB):
            semanticNetwork = SemanticNetwork(objectMap)
            yield semanticNetwork
            for altNetwork in semanticNetwork.generateAlternatives():
                yield altNetwork

    @staticmethod
    def iterObjectAssignment(figureA, figureB):
        for objectMap in CorrespondenceGeneratorWithAddRemove(figureA.objects,
                                                              figureB.objects):
            yield objectMap
