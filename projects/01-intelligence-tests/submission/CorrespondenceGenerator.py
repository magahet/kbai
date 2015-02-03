import itertools


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
