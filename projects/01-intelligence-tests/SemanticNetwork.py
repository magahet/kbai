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
            semanticNetwork = SemanticNetwork(objectMap)
            yield semanticNetwork
            for altNetwork in semanticNetwork.generateAlternatives():
                yield altNetwork

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
        'rotate': 2,
        'add': 5,
        'remove': 5,
        'change shape': 5,
    }

    orientationSet = set([
        'inside',
        'above',
        'left-of',
    ])

    def __init__(self, objectMap):
        '''Initialize the network using a given objectMap.'''
        self.attribHandlers = {
            'shape': self.shapeChange,
            'fill': self.fillChange,
            'size': self.sizeChange,
            'angle': self.angleChange,
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
            for name, _ in transforms:
                score += self.differenceWeights.get(name, 1)
        return score

    def generateAlternatives(self):
        for i in []:
            yield None
        #for objId, transforms in self.transforms.items():

    def parseOrientations(self, objectMap):
        newObjectMap = {}
        orientationList = {}
        for objId, (beforeObj, afterObj) in enumerate(objectMap):
            if afterObj is not None:
                newObjectMap[afterObj.name] = objId
        for objId, (beforeObj, afterObj) in enumerate(objectMap):
            orientationList[objId] = {}
            if afterObj is None:
                continue
            afterAttribs = self.parseAttribs(afterObj)
            for orientation in self.orientationSet.intersection(afterAttribs.keys()):
                orientationList[objId][orientation] = [
                    newObjectMap[k] for
                    k in afterAttribs[orientation].split(',') if
                    k in newObjectMap
                ]
        return orientationList

    def parseTransforms(self, objectMap):
        transformList = {}
        for objId, (beforeObj, afterObj) in enumerate(objectMap):
            if beforeObj is None:
                transformList[objId] = [('add', None)]
                continue
            elif afterObj is None:
                transformList[objId] = [('remove', None)]
                continue
            beforeAttribs = self.parseAttribs(beforeObj)
            afterAttribs = self.parseAttribs(afterObj)
            transforms = []
            #print beforeAttribs, afterAttribs
            for attribName in self.attribHandlers.iterkeys():
                transform = self.attribHandlers[attribName](beforeAttribs.get(attribName, ''),
                                                            afterAttribs.get(attribName, ''))
                if transform is not None:
                    transforms.append(transform)
            transformList[objId] = transforms
        return transformList

    @staticmethod
    def parseAttribs(obj):
        return {a.name: a.value for a in obj.attributes}

    def shapeChange(self, before, after):
        if before != after:
            return ('change shape', after)

    def fillChange(self, before, after):
        if before == after:
            return None
        beforeList = before.split(',')
        afterList = after.split(',')
        return ('fill', [f for f in afterList if f not in beforeList])

    def sizeChange(self, before, after):
        if before != after:
            if before == 'small':
                return ('expand', after)
            else:
                return ('contract', after)

    def angleChange(self, before, after):
        if before != after:
            return ('rotate', int(after) - int(before))


class FigureGenerator(object):
    '''A generator of RPM figures from a semantic network.'''

    def __init__(self, figure, semanticNetwork):
        '''Initialize the generator from a provided semantic network.'''
        self.figure = parseFigure(figure)
        self.semanticNetwork = semanticNetwork
        self.transformHandlers = {
            'fill': self.fill,
            'unfill': lambda x, v: ('fill', 'no'),
            'expand': lambda x, v: ('size', 'large'),
            'contract': lambda x, v: ('size', 'small'),
            'change shape': lambda x, v: ('shape', 'any'),
        }

    def __iter__(self):
        for objectMap in CorrespondenceGenerator(self.figure.keys(),
                                                 self.semanticNetwork.objectIds):
            yield self.transformFigure(objectMap)

    @staticmethod
    def fill(figObj, value):
        fillList = [f for f in figObj.get('fill', '').split(',') if f not in ['no']]
        for fill in value:
            if fill not in fillList:
                fillList.append(fill)
        return ('fill', ','.join(fillList))

    def transformFigure(self, objectMap):
        figure = {}
        netToFigObjMap = {netObjId: figObjId for
                          figObjId, netObjId in objectMap if
                          ('remove', None) not in self.semanticNetwork.transforms.get(netObjId)
                          }
        for figObjId, netObjId in objectMap:
            if ('remove', None) in self.semanticNetwork.transforms.get(netObjId):
                continue
            figObj = self.figure.get(figObjId)
            attributes = {}
            for transform, transformValue in self.semanticNetwork.transforms.get(netObjId, []):
                if transform.startswith('rotate'):
                    currentAngle = int(figObj.get('angle', 0))
                    attributes['angle'] = str(currentAngle + transformValue)
                elif transform not in self.transformHandlers:
                    continue
                else:
                    attribute, value = self.transformHandlers[transform](figObj, transformValue)
                    attributes[attribute] = value
            orientations = self.semanticNetwork.orientations.get(netObjId)
            attributes['shape'] = figObj.get('shape')
            for orientation, objIds in orientations.iteritems():
                attributes[orientation] = ','.join([netToFigObjMap[objId] for
                                                    objId in objIds if
                                                    objId in netToFigObjMap])
                #print orientation, attributes[orientation]
            # TODO figure out why this is needed
            for attribute in figObj:
                if attribute in attributes or attribute in ['above', 'inside', 'left-of']:
                    continue
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
