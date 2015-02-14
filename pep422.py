class Meta(type):
    @classmethod
    def __prepare__(cls, name, bases, namespace=None, **kwds):
        if namespace is not None:
            cls.__namespace__ = namespace
        if hasattr(cls, '__namespace__'):
            return cls.__namespace__()
        else:
            return super().__prepare__(name, bases, **kwds)

    def __new__(cls, name, bases, dict, **kwds):
        if '__init_class__' in dict:
            dict['__init_class__'] = classmethod(dict['__init_class__'])
        return super(Meta, cls).__new__(cls, name, bases, dict)

    def __init__(self, name, bases, dict, **kwds):
        self.__init_class__(**kwds)


def __init_class__(cls, **kwds):
    pass

WithInit = Meta("WithInit", (object,), dict(__init_class__=__init_class__))

# black magic: assure everyone is using the same WithInit
import sys
if hasattr(sys, "WithInit"):
    WithInit = sys.WithInit
else:
    sys.WithInit = WithInit
