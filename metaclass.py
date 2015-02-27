class Meta(type):
    @classmethod
    def __prepare__(cls, name, bases, namespace=None, **kwargs):
        if namespace is not None:
            cls.__namespace__ = namespace
        if hasattr(cls, '__namespace__'):
            return cls.__namespace__()
        else:
            return super().__prepare__(name, bases, **kwargs)

    def __new__(cls, name, bases, dict, **kwargs):
        return super(Meta, cls).__new__(cls, name, bases, dict)

    def __init__(self, name, bases, dict, namespace=None, **kwargs):
        super(self, self).__init_subclass__(**kwargs)


class Base(object):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        pass

SubclassInit = Meta("SubclassInit", (Base,), {})

