
from metaclass import SubclassInit


class Registry(SubclassInit):
    """ A simple registry registering all its base classes """
    subclasses = []

    def __init_subclass__(cls, ns, **kwargs):
        super(Registry, cls).__init_subclass__(ns, **kwargs)
        Registry.subclasses.append(cls)


class A(Registry):
    pass

print(Registry.subclasses)  # print [<class A>]
