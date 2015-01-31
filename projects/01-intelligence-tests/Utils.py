import sys
import itertools


def parseFigure(figureObj):
    figure = {}
    for obj in figureObj.objects:
        figure[obj.name] = {a.name: a.value for a in obj.attributes}
    #print figure
    return figure


def findFigureMatch(figure, choices):
    bestMatch = None
    bestScore = sys.maxint
    for choiceId, choice in choices.iteritems():
        # DEBUG
        #if choiceId != '6':
            #continue
        score = figuresMatch(figure, choice)
        if score < bestScore:
            bestMatch = choiceId
            bestScore = score
        if bestScore == 0:
            break
    return bestMatch, bestScore


def figuresMatch(figure1, figure2):
    figure1 = figure1 if isinstance(figure1, dict) else parseFigure(figure1)
    figure2 = figure2 if isinstance(figure2, dict) else parseFigure(figure2)
    if figure1 == figure2:
        return 0
    bestScore = sys.maxint
    for objectMap in CorrespondenceGenerator(figure1.keys(), figure2.keys()):
        #print '=' * 80
        #print objectMap
        score = 0
        for objId1, objId2 in objectMap:
            obj1Remapped = remapReferences(figure1.get(objId1, {}), dict(objectMap))
            score += compareObjects(obj1Remapped,
                                    figure2.get(objId2, {}))
        #print score
        if score < bestScore:
            bestScore = score
    return bestScore


def remapReferences(obj, objMap):
    newObj = {}
    for attrib in obj:
        if attrib in ['inside', 'above', 'left-of']:
            oldValues = obj[attrib].split(',')
            newObj[attrib] = ','.join(sorted([objMap[v] for v in oldValues if v in objMap]))
        else:
            newObj[attrib] = obj[attrib]
    return newObj


def compareObjects(obj1, obj2):
    #print obj1
    #print obj2
    score = 0
    for attrib in set(obj1.keys()).union(obj2.keys()):
        #print attrib, obj1.get(attrib, ''), obj2.get(attrib, '')
        if attrib == 'shape' and obj1.get('shape', '') == 'any':
            continue
        if obj1.get(attrib, '') != obj2.get(attrib, ''):
            score += 1
    return score


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
