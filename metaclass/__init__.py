"""
:mod:`metaclass` -- Writing and using metaclasses
=================================================

Metaclasses are a very powerful tool in Python. You can control
the entire class creation process with them.

Most of the time, however, they are too powerful. This module helps
you to use some of the advantages of metaclasses, without having
to know all the details.

Initializing subclasses
-----------------------

A very common usecase for a metaclass is that you just want to execute
some code after a class is created. This can easily done with
:class:`SubclassInit`. You just define a method ``__init_subclass__``,
which is implicitly considered a ``@classmethod`` and
will be called after each subclass that is generated of your
class. As a parameter it gets the the namespace of the class. An
example is a simple subclass registration::

    class Register(SubclassInit):
        subclasses = {}

        def __init_subclass__(cls, ns, **kwargs):
            super().__init_subclass__(ns, **kwargs)
            Register.subclasses[cls.__name__] = cls

Note how you can add keyword arguments. Those are the keyword
arguments given on the class definition line, as in::

    class Subclass(Register, spam="ham"):
        pass

Don't forget to properly call super()! Other classes may want to
initialize subclasses as well. This is also why you should pass over
the keyword arguments, just taking out the ones you need.

"""
from collections import OrderedDict

__all__ = ["SubclassInit"]

class Meta(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return OrderedDict()

    def __init__(self, name, bases, ns, **kwargs):
        if "__init_subclass__" in ns:
            self.__init_subclass__ = classmethod(ns["__init_subclass__"])
        super(self, self).__init_subclass__(ns, **kwargs)
        super(Meta, self).__init__(name, bases, ns)


class _Base(object):
    @classmethod
    def __init_subclass__(cls, ns):
        pass

SubclassInit = Meta("SubclassInit", (_Base,), {})
