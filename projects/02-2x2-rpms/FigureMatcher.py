import sys
from CorrespondenceGenerator import CorrespondenceGeneratorWithAddRemove


def parseFigure(figureObj):
    figure = {}
    for obj in figureObj.objects:
        figure[obj.name] = {a.name: a.value for a in obj.attributes}
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
    for objectMap in CorrespondenceGeneratorWithAddRemove(figure1.keys(), figure2.keys()):
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
            newObj[attrib] = ','.join(sorted([objMap[v] for v in oldValues if v in objMap and objMap[v] is not None]))
        else:
            newObj[attrib] = obj[attrib]
    return newObj


def compareObjects(obj1, obj2):
    score = 0
    for attrib in set(obj1.keys()).union(obj2.keys()):
        if obj1.get(attrib, '') != obj2.get(attrib, ''):
            score += 10
    return score


def compareShapes(shape1, shape2):
    angles = {
        'triangle': 3,
        'square': 4,
        'pentagon': 5,
        'hexagon': 6,
        'heptagon': 7,
        'octagon': 8,
    }
    if shape1 not in angles or shape2 not in angles:
        return 0 if shape1 == shape2 else 9
    return abs(angles[shape1] - angles[shape2])
