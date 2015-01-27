def parseFigure(figureObj):
    figure = {}
    for obj in figureObj.objects:
        figure[obj.name] = {a.name: a.value for a in obj.attributes}
    #print figure
    return figure


def findFigureMatch(figure, choices):
    print figure
    for choiceId, choice in choices.iteritems():
        if figuresMatch(figure, choice):
            print 'match found:', choiceId
            return choiceId


def figuresMatch(figure1, figure2):
    figures = []
    for num, fig in enumerate([figure1, figure2]):
        figures.append(fig if isinstance(fig, dict) else parseFigure(fig))
    return figures[0] == figures[1]
