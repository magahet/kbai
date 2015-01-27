'''This module provides a class for generating semantic networks for RPMs.'''


class SemanticNetworkGenerator(object):
    '''Represents a generator of semantic networks for RPMs.'''

    def __init__(self, problem):
        '''Initialize the generator from a provided RPM'''
        self.problem = problem

    def __iter__(self):
        figureA = self.problem.figures.get('A')
        figureB = self.problem.figures.get('B')
        for objectMap in self.iterObjectAssignment(figureA, figureB):
            yield SemanticNetwork(objectMap)

    @staticmethod
    def iterObjectAssignment(figureA, figureB):
        yield zip(figureA.objects, figureB.objects)


class SemanticNetwork(object):
    '''Represents a semantic network for RPMs.'''

    def __init__(self, objectMap):
        '''Initialize the network using a given objectMap.'''
        self.attribHandlers = {
            'shape': self.shapeChange,
            'fill': self.fillChange,
        }
        self.orientations = self.parseOrientations(objectMap)
        self.transforms = self.parseTransforms(objectMap)

    def __repr__(self):
        return '''SemanticNetwork(orientations={}, transformations={})'''.format(
            str(self.orientations),
            str(self.transforms),
        )

    def parseOrientations(self, objectMap):
        pass

    def parseTransforms(self, objectMap):
        transformLists = []
        for beforeObj, afterObj in objectMap:
            beforeAttribs = self.parseAttribs(beforeObj)
            afterAttribs = self.parseAttribs(afterObj)
            transforms = []
            for attribName in self.attribHandlers.iterkeys():
                transform = self.attribHandlers[attribName](beforeAttribs.get(attribName),
                                                            afterAttribs.get(attribName))
                if transform is not None:
                    transforms.append(transform)
            if transforms:
                transformLists.append(transforms)
        return transformLists

    @staticmethod
    def parseAttribs(obj):
        return {a.name: a.value for a in obj.attributes}

    def shapeChange(self, before, after):
        if before != after:
            return 'shape change'

    def fillChange(self, before, after):
        if before != after:
            if before == 'no':
                return 'fill'
            else:
                return 'unfill'
