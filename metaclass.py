class Meta(type):
    @classmethod
    def __prepare__(cls, name, bases, namespace=None, **kwargs):
        for b in bases:
            if isinstance(b, Meta) and hasattr(b, "__namespace__"):
                return b.__namespace__()
        return super().__prepare__(name, bases, **kwargs)

    def __new__(cls, name, bases, dict, **kwargs):
        method = dict.get("__init_subclass__")
        if method is not None:
            dict["__init_subclass__"] = classmethod(method)
        return super(Meta, cls).__new__(cls, name, bases, dict)

    def __init__(self, name, bases, dict, namespace=None, **kwargs):
        super(self, self).__init_subclass__(**kwargs)
        if namespace is not None:
            self.__namespace__ = namespace


class Base(object):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        pass

SubclassInit = Meta("SubclassInit", (Base,), {})

