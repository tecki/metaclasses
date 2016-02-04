from metaclass import SubclassInit
import weakref

class WeakAttribute:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]()

    def __set__(self, instance, value):
        instance.__dict__[self.name] = weakref.ref(value)

    def __init_descriptor__(self, owner, name):
        self.name = name

class Test(SubclassInit):
    a = WeakAttribute()

t = Test()
t.a = {3}
assert t.a is None
a = {4}
t.a = a
assert t.a == {4}
del a
assert t.a is None
