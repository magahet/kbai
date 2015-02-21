from CorrespondenceGenerator import CorrespondenceGeneratorWithAddRemove


class FigureGenerator(object):
    '''A generator of RPM figures from a semantic network.'''

    positions = ['above', 'inside', 'left-of', 'overlaps']

    def __init__(self, figure, semanticNetwork):
        '''Initialize the generator from a provided semantic network.'''
        self.figure = self.parseFigure(figure)
        self.semanticNetwork = semanticNetwork
        self.transformHandlers = {
            'fill': self.fill,
            'unfill': lambda x, v: ('fill', 'no'),
            'change size': self.changeSize,
            'rotate': self.rotate,
            'change shape': lambda x, v: ('shape', v),
            'vertical-flip': lambda x, v: ('vertical-flip', v),
        }

    def __iter__(self):
        #print self.figure.keys()
        #print self.semanticNetwork.objectIds
        for objectMap in CorrespondenceGeneratorWithAddRemove(
            self.figure.keys(),
                self.semanticNetwork.objectIds):
            #print objectMap
            result = self.transformFigure(objectMap)
            if result is None:
                continue
            yield result

    @staticmethod
    def changeSize(figObj, value):
        '''Change the size of the object.'''
        before, after = value
        # Raise an exception if the current size does not match the transform
        # before size.
        if figObj.get('size', '') != before:
            #print 'bad'
            raise Exception
        #print 'good'
        return ('size', after)

    @staticmethod
    def rotate(figObj, value):
        currentAngle = int(figObj.get('angle', 0))
        return ('angle', str((currentAngle + value) % 360))

    @staticmethod
    def fill(figObj, value):
        fillList = [f for f in
                    figObj.get('fill', '').split(',') if
                    f not in ['no']]
        for fill in value:
            if fill not in fillList:
                fillList.append(fill)
        return ('fill', ','.join(fillList))

    def transformFigure(self, objectMap):
        figure = {}
        netToFigObjMap = {
            netObjId: figObjId for
            figObjId, netObjId in objectMap if
            netObjId is not None and 'remove' not in self.semanticNetwork.transforms.get(netObjId)
        }
        for num, (figObjId, netObjId) in enumerate(objectMap):
            if 'remove' in self.semanticNetwork.transforms.get(netObjId, {}):
                continue
            if 'add' in self.semanticNetwork.transforms.get(netObjId, {}):
                figure[str(num)] = {}
                for attrib, value in self.semanticNetwork.transforms.get(netObjId, {}).get('add', {}).iteritems():
                    if attrib in self.positions:
                        if isinstance(value, list):
                            #print 'blah', [netToFigObjMap.get(o, '') for o in value]
                            figure[str(num)][attrib] = ','.join(sorted([netToFigObjMap.get(o, '') for o in value if netToFigObjMap.get(o, '') is not None]))
                    else:
                        figure[str(num)][attrib] = value
                continue
            figObj = self.figure.get(figObjId)
            if figObj is None or 'shape' not in figObj:
                continue
            attributes = {}
            transforms = self.semanticNetwork.transforms.get(netObjId, {})
            for transform, transformValue in transforms.iteritems():
                if transform not in self.transformHandlers:
                    continue
                else:
                    try:
                        attribute, value = self.transformHandlers[transform](
                            figObj, transformValue)
                        attributes[attribute] = value
                    except:
                        return None
            positions = self.semanticNetwork.positions['after'].get(netObjId, {})
            for position, objIds in positions.iteritems():
                positionList = [netToFigObjMap[objId] for
                                objId in objIds if
                                objId is not None and objId in netToFigObjMap]
                attributes[position] = ','.join(
                    sorted([p for p in positionList if p is not None]))
            for attribute in figObj:
                if attribute in attributes or attribute in self.positions:
                    continue
                attributes[attribute] = figObj.get(attribute)
            figure[figObjId] = attributes
        return figure, self.positionsMatch(netToFigObjMap)

    def positionsMatch(self, netToFigObjMap):
        netPositions = self.semanticNetwork.positions.get('before', {})
        score = 0
        for objId, figObjId in netToFigObjMap.iteritems():
            for position in ['inside', 'above', 'left-of', 'overlaps']:
                netValues = set([netToFigObjMap[o] for
                                o in netPositions.get(objId, {}).get(
                                    position, []) if
                                o in netToFigObjMap])
                figValues = set([o for
                                 o in self.figure.get(figObjId, {}).get(
                                     position, '').split(',') if o])
                score += len(netValues.symmetric_difference(figValues))
        return score

    @staticmethod
    def parseFigure(figureObj):
        figure = {}
        for obj in figureObj.objects:
            figure[obj.name] = {a.name: a.value for a in obj.attributes}
        return figure
