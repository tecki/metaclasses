metaclass - Writing and using metaclasses
==========================================

Metaclasses are a very powerful tool in Python. You can control
the entire class creation process with them.

Most of the time, however, they are too powerful. This module helps
you to use some of the advantages of metaclasses, without having
to know all the details. It defines a base class `SubclassInit`.
Inheriting from this class one can modify the subclass creation
process.

Initializing subclasses
-----------------------

A very common usecase for a metaclass is that you just want to execute
some code after a class is created. This can easily done with
``SubclassInit``. You just define a method ``__init_subclass__``,
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

Don't forget to properly call ``super()``! Other classes may want to
initialize subclasses as well. This is also why you should pass over
the keyword arguments, just taking out the ones you need.

Initializing Descriptors
------------------------

Descriptors are a powerful technique to create object attributes which
calculate their value on-the-fly. A property is a simple example of such
a descriptor. There is a common problem with those descriptors: they
do not know their name. Using ``SubclassInit`` you can add an
``__init_descriptor__`` method to a descriptor which gets called once the
class is ready and the descriptor's name is known.

As an example, we can define a descriptor which makes an attribute a
weak reference::

    import weakref

    class WeakAttribute:
        def __get__(self, instance, owner):
            return instance.__dict__[self.name]()

        def __set__(self, instance, value):
            instance.__dict__[self.name] = weakref.ref(value)

        def __init_descriptor__(self, owner, name):
            self.name = name

Order of Attributes
-------------------

Sometimes one is interested in which order the attributes were defined
in the class. ``SubclassInit`` leaves a tuple with all the names of the
attributes in the order they were defined as a class attribute called
``__attribute_order__``. Note that Python already defines some class
attributes, like ``__module__``, some of which also show up in this
tuple.

As an example::

    class AttributeOrder(SubclassInit):
        a = 1

        def b(self):
            pass

        c = 5

    assert AttributeOrder.__attribute_order__ == \
        ('__module__', '__qualname__', 'a', 'b', 'c')
