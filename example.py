
from pep422 import SubclassInit


class Registry(SubclassInit):
    """ A simple registry registering all its base classes """
    subclasses = []

    @classmethod
    def __init_subclass__(cls):
        Registry.subclasses.append(cls)


class A(Registry):
    pass

print(Registry.subclasses)  # print [<class A>]
