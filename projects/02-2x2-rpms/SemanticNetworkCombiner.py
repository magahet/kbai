from CorrespondenceGenerator import CorrespondenceGeneratorWithAddRemove
from SemanticNetwork import SemanticNetwork


class SemanticNetworkCombiner(object):
    '''A combiner of semantic networks for RPMs.'''

    def __init__(self, network1, network2):
        '''Initialize the generator from two provided networks'''
        self.network1 = network1
        self.network2 = network2
        #print 'A:B', self.network1
        #print 'A:C', self.network2
        self.attribHandlers = {
            'rotate': lambda x, y: (x + y) % 360,
        }

    def __iter__(self):
        for objectMap in CorrespondenceGeneratorWithAddRemove(
                self.network1.objectIds, self.network2.objectIds):
            positions, transforms = self.combineNetworks(objectMap)
            semanticNetwork = SemanticNetwork(positions, transforms)
            yield semanticNetwork
            for altNetwork in semanticNetwork.generateAlternatives():
                yield altNetwork
            #semanticNetwork = SemanticNetwork(self.network2.positions, transforms)
            #yield semanticNetwork
            #for altNetwork in semanticNetwork.generateAlternatives():
                #yield altNetwork
        # missing original net against other net alternatives
        for altNet1 in self.network1.generateAlternatives():
            for altNet2 in self.network2.generateAlternatives():
                for objectMap in CorrespondenceGeneratorWithAddRemove(altNet1.objectIds, altNet2.objectIds):
                    positions, transforms = self.combineNetworks(objectMap)
                    semanticNetwork = SemanticNetwork(positions, transforms)
                    yield semanticNetwork
                    for altNetwork in semanticNetwork.generateAlternatives():
                        yield altNetwork
                    #semanticNetwork = SemanticNetwork(self.network2.positions, transforms)
                    #yield semanticNetwork
                    #for altNetwork in semanticNetwork.generateAlternatives():
                        #yield altNetwork

    def combineNetworks(self, objectMap):
        positions = self.network1.positions
        transforms = {}
        #print objectMap
        for newObjId, (objId1, objId2) in enumerate(objectMap):
            transforms[newObjId] = {}
            t1 = self.network1.transforms.get(objId1, {})
            t2 = self.network2.transforms.get(objId2, {})
            #print t1, t2
            if 'add' in t1:
                transforms[objId1 + 10] = t1
                t1 = {}
            if 'add' in t2:
                transforms[objId2 + 20] = t2
                t2 = {}
            #print 't1', t1
            #print 't2', t2
            for attrib in set(t1.keys()).union(t2.keys()):
                transforms[newObjId][attrib] = self.combineAttribs(
                    attrib, t1.get(attrib), t2.get(attrib))
            #print 'new', transforms[newObjId]
        return positions, transforms

    def combineAttribs(self, attrib, t1, t2):
        if None in (t1, t2):
            return t1 if t1 is not None else t2
        elif attrib in self.attribHandlers:
            return self.attribHandlers[attrib](t1, t2)
        else:
            return t1
