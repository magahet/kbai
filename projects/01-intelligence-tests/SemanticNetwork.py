import itertools


class SemanticNetwork(object):
    '''A semantic network for RPMs.'''

    differenceWeights = {
        None: 0,
        'fill': 1,
        'unfill': 1,
        'change size': 1,
        'rotate': 2,
        'flip': 3,
        'vertical-flip': -1,
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
            'vertical-flip': self.verticalFlip,
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
            for name, _ in transforms.iteritems():
                score += self.differenceWeights.get(name, 1)
        return score

    def generateAlternatives(self):
        # Horizontal flips
        flips = [objId for
                 objId, transforms in self.transforms.iteritems() if
                 transforms.get('rotate', 0) == 180]
        for num in range(1, len(flips) + 1):
            for objIds in itertools.combinations(flips, num):
                for objId in objIds:
                    del self.transforms[objId]['rotate']
                    self.transforms[objId]['flip'] = 'horizontal'
                yield self
                for objId in objIds:
                    self.transforms[objId]['rotate'] = 180
                    del self.transforms[objId]['flip']

        # Vertical flips
        for num in range(1, len(flips) + 1):
            for objIds in itertools.combinations(flips, num):
                for objId in objIds:
                    flipValue = self.transforms[objId].get('vertical-flip', 'no')
                    flipValue = 'yes' if flipValue == 'no' else 'no'
                    self.transforms[objId]['vertical-flip'] = flipValue
                    #rotateValue = self.transforms[objId]['rotate']
                    #self.transforms[objId]['rotate'] = (rotateValue + 180) % 360
                yield self
                for objId in objIds:
                    flipValue = self.transforms[objId].get('vertical-flip', 'no')
                    flipValue = 'yes' if flipValue == 'no' else 'no'
                    self.transforms[objId]['vertical-flip'] = flipValue
                    #rotateValue = self.transforms[objId]['rotate']
                    #self.transforms[objId]['rotate'] = (rotateValue + 180) % 360

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
                transformList[objId] = {'add': None}
                continue
            elif afterObj is None:
                transformList[objId] = {'remove': None}
                continue
            beforeAttribs = self.parseAttribs(beforeObj)
            afterAttribs = self.parseAttribs(afterObj)
            transforms = {}
            print beforeAttribs, afterAttribs
            for attribName in self.attribHandlers.iterkeys():
                result = self.attribHandlers[attribName](beforeAttribs.get(attribName, ''),
                                                         afterAttribs.get(attribName, ''))
                if result is not None:
                    transform, value = result
                    transforms[transform] = value
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

    def verticalFlip(self, before, after):
        if before != after:
            return ('vertical-flip', after)
