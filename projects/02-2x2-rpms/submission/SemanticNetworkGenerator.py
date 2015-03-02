from CorrespondenceGenerator import CorrespondenceGeneratorWithAddRemove
from SemanticNetwork import SemanticNetwork


class SemanticNetworkGenerator(object):
    '''A generator of semantic networks for RPMs.'''

    def __init__(self, problem, source='A', target='B'):
        '''Initialize the generator from a provided RPM'''
        self.problem = problem
        self.source = source
        self.target = target

    def __iter__(self):
        figureA = self.problem.figures.get(self.source)
        figureB = self.problem.figures.get(self.target)
        for objectMap in self.iterObjectAssignment(figureA, figureB):
            semanticNetwork = SemanticNetwork()
            semanticNetwork.buildFromObjectMap(objectMap)
            yield semanticNetwork
            for altNetwork in semanticNetwork.generateAlternatives():
                yield altNetwork

    @staticmethod
    def iterObjectAssignment(figureA, figureB):
        for objectMap in CorrespondenceGeneratorWithAddRemove(figureA.objects,
                                                              figureB.objects):
            yield objectMap
