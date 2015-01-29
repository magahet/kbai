'''A module for generating semantic networks for RPMs.'''

import itertools
from Utils import parseFigure


class SemanticNetworkGenerator(object):
    '''A generator of semantic networks for RPMs.'''

    def __init__(self, problem):
        '''Initialize the generator from a provided RPM'''
        self.problem = problem

    def __iter__(self):
        figureA = self.problem.figures.get('A')
        figureB = self.problem.figures.get('B')
        for objectMap in self.iterObjectAssignment(figureA, figureB):
            #print objectMap
            yield SemanticNetwork(objectMap)

    @staticmethod
    def iterObjectAssignment(figureA, figureB):
        for objectMap in CorrespondenceGeneratorWithAddRemove(figureA.objects,
                                                              figureB.objects):
            yield objectMap


class SemanticNetwork(object):
    '''A semantic network for RPMs.'''

    differenceWeights = {
        None: 0,
        'fill': 1,
        'unfill': 1,
        'expand': 1,
        'contract': 1,
        'add': 5,
        'remove': 5,
        'change shape': 5,
    }

    orientationSet = set([
        'inside',
    ])

    def __init__(self, objectMap):
        '''Initialize the network using a given objectMap.'''
        self.attribHandlers = {
            'shape': self.shapeChange,
            'fill': self.fillChange,
            'size': self.sizeChange,
        }
        self.orientations = self.parseOrientations(objectMap)
        self.transforms = self.parseTransforms(objectMap)

    def __repr__(self):
        return '''SemanticNetwork(orientations={}, transformations={})'''.format(
            str(self.orientations),
            str(self.transforms),
        )

    @property
    def objectIds(self):
        return self.transforms.keys()

    @property
    def score(self):
        score = 0
        for objId, transforms in self.transforms.iteritems():
            for name in transforms:
                score += self.differenceWeights.get(name)
        return score

    def parseOrientations(self, objectMap):
        pass
        #newObjectMap = defaultdict(dict)
        #orientationList = {}
        #for objId, (beforeObj, afterObj) in enumerate(objectMap):
            #newObjectMap[beforeObj.name] = objId

            #if afterObj is None:
                #continue
            #afterAttribs = self.parseAttribs(afterObj)
            #orientationList[objId] = afterObj

    def parseTransforms(self, objectMap):
        transformList = {}
        for objId, (beforeObj, afterObj) in enumerate(objectMap):
            if beforeObj is None:
                transformList[objId] = ['add']
                continue
            elif afterObj is None:
                transformList[objId] = ['remove']
                continue
            beforeAttribs = self.parseAttribs(beforeObj)
            afterAttribs = self.parseAttribs(afterObj)
            transforms = []
            print beforeAttribs, afterAttribs
            for attribName in self.attribHandlers.iterkeys():
                transform = self.attribHandlers[attribName](beforeAttribs.get(attribName),
                                                            afterAttribs.get(attribName))
                if transform is not None:
                    transforms.append(transform)
            transformList[objId] = transforms
        return transformList

    @staticmethod
    def parseAttribs(obj):
        return {a.name: a.value for a in obj.attributes}

    def shapeChange(self, before, after):
        if before != after:
            return 'change shape'

    def fillChange(self, before, after):
        if before != after:
            if before == 'no':
                return 'fill'
            else:
                return 'unfill'

    def sizeChange(self, before, after):
        if before != after:
            if before == 'small':
                return 'expand'
            else:
                return 'contract'


class FigureGenerator(object):
    '''A generator of RPM figures from a semantic network.'''

    def __init__(self, figure, semanticNetwork):
        '''Initialize the generator from a provided semantic network.'''
        self.figure = parseFigure(figure)
        self.semanticNetwork = semanticNetwork
        self.transformHandlers = {
            'fill': lambda x: ('fill', 'yes'),
            'unfill': lambda x: ('fill', 'no'),
            'expand': lambda x: ('size', 'large'),
            'contract': lambda x: ('size', 'small'),
        }

    def __iter__(self):
        for objectMap in CorrespondenceGenerator(self.figure.keys(),
                                                 self.semanticNetwork.objectIds):
            yield self.transformFigure(objectMap)

    def transformFigure(self, objectMap):
        figure = {}
        for figObjId, netObjId in objectMap:
            figObj = self.figure.get(figObjId)
            attributes = {}
            for transform in self.semanticNetwork.transforms.get(netObjId):
                if transform == 'remove':
                    break
                if transform not in self.transformHandlers:
                    continue
                attribute, value = self.transformHandlers[transform](figObj)
                attributes[attribute] = value
            else:
                for attribute in set(figObj.keys()).difference(attributes.keys()):
                    attributes[attribute] = figObj.get(attribute)
                figure[figObjId] = attributes
        return figure


class CorrespondenceGenerator(object):
    '''A generator of ways to match items between two lists.'''

    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2

    def __iter__(self):
        for reorderedList in itertools.permutations(self.list1,
                                                    len(self.list2)):
            yield zip(reorderedList, self.list2)


class CorrespondenceGeneratorWithAddRemove(object):
    '''A generator of ways to match items between two lists.'''

    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2

    def __iter__(self):
        if len(self.list1) > len(self.list2):
            longList = self.list1
            shortList = self.list2
            reverse = False
        else:
            longList = self.list2
            shortList = self.list1
            reverse = True
        for reorderedList in itertools.permutations(longList,
                                                    len(longList)):
            if reverse:
                yield [i for i in itertools.izip_longest(shortList, reorderedList)]
            else:
                yield [i for i in itertools.izip_longest(reorderedList, shortList)]
