'''A module for generating semantic networks for RPMs.'''

from Utils import (parseFigure, CorrespondenceGenerator, CorrespondenceGeneratorWithAddRemove)
import itertools


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
        'change size': 1,
        'rotate': 2,
        'flip': 1,
        'add': 5,
        'remove': 5,
        'change shape': 5,
    }

    positionSet = set([
        'inside',
        'above',
        'left-of',
        'overlaps'
    ])

    def __init__(self, objectMap):
        '''Initialize the network using a given objectMap.'''
        self.attribHandlers = {
            'shape': self.shapeChange,
            'fill': self.fillChange,
            'size': self.sizeChange,
            'angle': self.angleChange,
        }
        self.positions = self.parsepositions(objectMap)
        self.transforms = self.parseTransforms(objectMap)

    def __repr__(self):
        return '''SemanticNetwork(positions={}, transformations={})'''.format(
            str(self.positions),
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
        flips = [(objId, transforms.index(('rotate', 180))) for
                 objId, transforms in self.transforms.iteritems() if
                 ('rotate', 180) in transforms]
        for num in range(1, len(flips) + 1):
            for objIdSets in itertools.combinations(flips, num):
                for objId, index in objIdSets:
                    self.transforms[objId][index] = ('flip', 'horizontal')
                yield self
                for objId, index in objIdSets:
                    self.transforms[objId][index] = ('rotate', 180)

    def parsepositions(self, objectMap):
        newObjectMapBefore = {}
        newObjectMapAfter = {}
        positionList = {'before': {}, 'after': {}}
        for objId, (beforeObj, afterObj) in enumerate(objectMap):
            if beforeObj is not None:
                newObjectMapBefore[beforeObj.name] = objId
            if afterObj is not None:
                newObjectMapAfter[afterObj.name] = objId
        for objId, (beforeObj, afterObj) in enumerate(objectMap):
            positionList['before'][objId] = {}
            positionList['after'][objId] = {}
            if beforeObj is not None:
                beforeAttribs = self.parseAttribs(beforeObj)
                for position in self.positionSet.intersection(beforeAttribs.keys()):
                    positionList['before'][objId][position] = [
                        newObjectMapBefore[k] for
                        k in beforeAttribs[position].split(',') if
                        k in newObjectMapBefore
                    ]
            if afterObj is not None:
                afterAttribs = self.parseAttribs(afterObj)
                for position in self.positionSet.intersection(afterAttribs.keys()):
                    positionList['after'][objId][position] = [
                        newObjectMapAfter[k] for
                        k in afterAttribs[position].split(',') if
                        k in newObjectMapAfter
                    ]
        return positionList

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
            return ('change size', (before, after))

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
            'change size': self.changeSize,
            'change shape': lambda x, v: ('shape', v),
            'flip': lambda x, v: ('rotate', x.get('rotate', '0')),
        }

    def __iter__(self):
        for objectMap in CorrespondenceGenerator(self.figure.keys(),
                                                 self.semanticNetwork.objectIds):
            #print objectMap
            result = self.transformFigure(objectMap)
            if result is None:
                continue
            yield result

    @staticmethod
    def changeSize(figObj, value):
        '''Change the size of the object.'''
        #print figObj.get('size')
        #print value
        before, after = value
        # Raise an exception if the current size does not match the transform before size
        if figObj.get('size', '') != before:
            #print 'bad'
            raise Exception
        #print 'good'
        return ('size', after)

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
                    try:
                        attribute, value = self.transformHandlers[transform](figObj, transformValue)
                        attributes[attribute] = value
                    except:
                        return None
            if attributes.get('shape', '') != 'any' and 'shape' not in attributes:
                attributes['shape'] = figObj.get('shape')
            positions = self.semanticNetwork.positions['after'].get(netObjId)
            for position, objIds in positions.iteritems():
                attributes[position] = ','.join(sorted([netToFigObjMap[objId] for
                                                        objId in objIds if
                                                        objId in netToFigObjMap]))
                #print position, attributes[position]
            # TODO figure out why this is needed
            for attribute in figObj:
                if attribute in attributes or attribute in ['above', 'inside', 'left-of', 'overlaps']:
                    continue
                attributes[attribute] = figObj.get(attribute)
            figure[figObjId] = attributes
        return figure, self.positionsMatch(netToFigObjMap)

    def positionsMatch(self, netToFigObjMap):
        netPositions = self.semanticNetwork.positions.get('before', {})
        #print netPositions
        #print netToFigObjMap
        score = 0
        for objId, figObjId in netToFigObjMap.iteritems():
            for position in ['inside', 'above', 'left-of', 'overlaps']:
                netValues = set([netToFigObjMap[o] for
                                o in netPositions.get(objId, {}).get(position, []) if
                                o in netToFigObjMap])
                figValues = set([o for
                                 o in self.figure.get(figObjId, {}).get(position, '').split(',') if o])
                #print netValues, figValues
                score += len(netValues.symmetric_difference(figValues))

        return score
