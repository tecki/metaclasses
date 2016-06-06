"""
:mod:`metaclass` -- Writing and using metaclasses
=================================================

Metaclasses are a very powerful tool in Python. You can control
the entire class creation process with them.

Most of the time, however, they are too powerful. This module helps
you to use some of the advantages of metaclasses, without having
to know all the details. It defines a base class `Object`.
Inheriting from this class one can modify the subclass creation
process.

Initializing subclasses
-----------------------

A very common usecase for a metaclass is that you just want to execute
some code after a class is created. This can easily done with
:class:`Object`. You just define a method ``__init_subclass__``,
which is implicitly considered a ``@classmethod`` and
will be called after each subclass that is generated of your
class. As a parameter it gets the namespace of the class. An example
is a simple subclass registration::

    class Register(Object):
        subclasses = []

        def __subclass_init__(cls, **kwargs):
            super().__subclass_init__(**kwargs)
            Register.subclasses.append(cls)

Note how you can add keyword arguments. Those are the keyword
arguments given on the class definition line, as in::

    class Subclass(Base, spam="ham"):
        pass

Don't forget to properly call super()! Other classes may want to
initialize subclasses as well. This is also why you should pass over
the keyword arguments, just taking out the ones you need.

Initializing Descriptors
------------------------

Descriptors are a powerful technique to create object attributes which
calculate their value on-the-fly. A property is a simple example of such
a descriptor. There is a common problem with those descriptors: they
do not know their name. Using `Object` you can add an
`__set_owner__` method to a descriptor which gets called once the
class is ready and the descriptor's name is known.

As an example, we can define a descriptor which makes an attribute a
weak reference::

    import weakref

    class WeakAttribute:
        def __get__(self, instance, owner):
            return instance.__dict__[self.name]()

        def __set__(self, instance, value):
            instance.__dict__[self.name] = weakref.ref(value)

        def __set_owner__(self, owner, name):
            self.name = name

Order of Attributes
-------------------

Sometimes one is interested in which order the attributes were defined
in the class. `Object` leaves a tuple with all the names of the
attributes in the order they were defined as a class attribute called
`__attribute_order__`. Note that Python already defines some class
attributes, like `__module__`, some of which also show up in this
tuple.

As an example::

    class AttributeOrder(Object):
        a = 1

        def b(self):
            pass

        c = 5

    assert AttributeOrder.__attribute_order__ == \
        ('__module__', '__qualname__', 'a', 'b', 'c')
"""

import abc
from collections import OrderedDict


__all__ = ["Type", "Object", "ABC", "ABCMeta"]


class Type(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return OrderedDict()

    def __new__(cls, name, bases, ns, **kwargs):
        method = ns.get("__init_subclass__")
        if method is not None:
            ns["__init_subclass__"] = classmethod(method)
        ns["__attribute_order__"] = tuple(ns.keys())
        ret = super(Type, cls).__new__(cls, name, bases, ns)
        super(ret, ret).__init_subclass__(**kwargs)
        return ret

    def __init__(self, name, bases, ns, **kwargs):
        super(Type, self).__init__(name, bases, ns)
        for k, v in ns.items():
            if hasattr(v, "__set_owner__"):
                v.__set_owner__(self, k)


class ABCMeta(Type, abc.ABCMeta):
    pass


class Base(object):
    @classmethod
    def __init_subclass__(cls):
        pass


Object = Type("Object", (Base,), {})
ABC = ABCMeta("ABC", (Base,), {})
