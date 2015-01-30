import sys


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
    score = 0
    for objId in set(figure1.keys()).union(figure2.keys()):
        obj1 = figure1.get(objId, {})
        obj2 = figure2.get(objId, {})
        for attrib in set(obj1.keys()).union(obj2.keys()):
            if obj1.get(attrib, '') != obj2.get(attrib, ''):
                score += 1
    return score
