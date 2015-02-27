
from metaclass import SubclassInit


class Registry(SubclassInit):
    """ A simple registry registering all its base classes """
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super(Registry, cls).__init_subclass__(**kwargs)
        Registry.subclasses.append(cls)


class A(Registry):
    pass

print(Registry.subclasses)  # print [<class A>]
