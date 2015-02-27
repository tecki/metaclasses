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
class. As a parameter it gets the namespace of the class. An example
is a simple subclass registration::

    class Register(SubclassInit):
        subclasses = []

        def __subclass_init__(cls, ns, **kwargs):
            super().__subclass_init__(ns, **kwargs)
            Register.subclasses.append(cls)

Note how you can add keyword arguments. Those are the keyword
arguments given on the class definition line, as in::

    class Subclass(Base, spam="ham"):
        pass

Don't forget to properly call super()! Other classes may want to
initialize subclasses as well. This is also why you should pass over
the keyword arguments, just taking out the ones you need.

Initializing Namespaces
-----------------------

Often the namespace is inspected in a subclass initializer. Sometimes
one would prefer that this is not a simple :class:`dict`, but something
more advanced. An :class:`collections.OrderedDict` comes to mind if one
is interested in the order things were defined in a class. This
can be achieved with the ``namespace`` keyword argument to the class
definition::

    class Register(SubclassInit, namespace=collections.OrderedDict):
        pass

Remember that the namespace holds for the subclasses, not the class itself!
"""
class Meta(type):
    @classmethod
    def __prepare__(cls, name, bases, namespace=None, **kwargs):
        for b in bases:
            if isinstance(b, Meta) and hasattr(b, "__namespace__"):
                return b.__namespace__()
        return super().__prepare__(name, bases, **kwargs)

    def __new__(cls, name, bases, ns, **kwargs):
        method = ns.get("__init_subclass__")
        if method is not None:
            ns["__init_subclass__"] = classmethod(method)
        return super(Meta, cls).__new__(cls, name, bases, ns)

    def __init__(self, name, bases, ns, namespace=None, **kwargs):
        super(Meta, self).__init__(name, bases, ns)
        super(self, self).__init_subclass__(ns, **kwargs)
        if namespace is not None:
            self.__namespace__ = namespace


class Base(object):
    @classmethod
    def __init_subclass__(cls, ns, **kwargs):
        pass

SubclassInit = Meta("SubclassInit", (Base,), {})
