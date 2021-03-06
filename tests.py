import abc
from metaclass import ABC, Object, Type
from unittest import TestCase, main
import types

class Test(TestCase):
    def test_classes(self):
        # PEP 422: Simple class initialisation hook
        class BaseC(Object):
            def __init_subclass__(cls):
                cls.x = 0
        class C(BaseC):
            pass
        self.assertEqual(0, C.x)
        # inherited:
        class D(C):
            pass
        self.assertEqual(0, D.__dict__['x'])
        # overwrite:
        class E(C):
            x = 1
        self.assertEqual(0, E.__dict__['x'])
        # override:
        class BaseF(C):
            def __init_subclass__(cls):
                cls.y = 1
        class F(BaseF):
            pass
        self.assertEqual(1, F.y)
        self.assertEqual(0, F.x)
        self.assertNotIn('x', F.__dict__)
        self.assertFalse(hasattr(C, 'y'))
        # super:
        class BaseG(C):
            def __init_subclass__(cls):
                super().__init_subclass__()
                cls.y = 1
        class G(BaseG):
            pass
        self.assertEqual(1, G.y)
        self.assertEqual(0, G.__dict__['x'])
        self.assertFalse(hasattr(C, 'y'))
        # __class__:
        class BaseI(Object):
            def __init_subclass__(cls):
                cls.x = 0
                __class__.y += 1
            y = 0
        class I(BaseI):
            pass
        self.assertEqual(0, I.x)
        self.assertEqual(1, I.y)
        class J(I):
            pass
        self.assertEqual(0, J.__dict__['x'])
        self.assertEqual(2, I.y)
        class BaseK(J):
            def __init_subclass__(cls):
                super().__init_subclass__()
                __class__.z += 1
            z = 0
        class K(BaseK):
            pass
        self.assertEqual(0, K.__dict__['x'])
        self.assertEqual(4, I.y)
        self.assertEqual(1, K.z)
        self.assertFalse(hasattr(J, 'z'))
        # multiple inheritance:
        class L(Object):
            def __init_subclass__(cls):
                pass
        class BaseM(L):
            def __init_subclass__(cls):
                super().__init_subclass__()
                cls.x = 0
        class M(BaseM):
            pass
        self.assertEqual(0, M.x)
        class BaseN(L):
            def __init_subclass__(cls):
                super().__init_subclass__()
                cls.y = 1
        class N(BaseN):
            pass
        self.assertEqual(1, N.y)
        class BaseO(M, N):
            def __init_subclass__(cls):
                super().__init_subclass__()
                cls.z = 2
        class O(BaseO):
            pass
        self.assertEqual(0, O.__dict__['x'])
        self.assertEqual(1, O.__dict__['y'])
        self.assertEqual(2, O.__dict__['z'])
        # decorators:
        def dec1(cls):
            cls.x = 1
            return cls
        def dec2(cls):
            cls.x = 2
            return cls
        @dec2
        @dec1
        class P:
            def __init_subclass__(cls):
                cls.x = 0
        self.assertEqual(2, P.x)
        # __init_subclass__ raises an exception:
        S = sentinel = object()
        with self.assertRaisesRegex(KeyError, 'xxx'):
            class BaseS(Object):
                def __init_subclass__(cls):
                    raise KeyError('xxx')
            class S(BaseS):
                pass
        self.assertIs(sentinel, S)

    def test_types(self):
        # PEP 422: Simple class initialisation hook
        def c(ns):
            def __init_subclass__(cls):
                cls.x = 0
            ns['__init_subclass__'] = __init_subclass__
        BaseC = types.new_class("BaseC", (Object,), exec_body=c)
        C = types.new_class("C", (BaseC,))
        self.assertEqual(C.x, 0)
        # inherited:
        D = types.new_class("D", (C,))
        self.assertEqual(D.__dict__['x'], 0)
        # overwrite:
        def e(ns):
            ns['x'] = 1
        E = types.new_class("E", (C,), exec_body=e)
        self.assertEqual(E.__dict__['x'], 0)
        # override:
        def f(ns):
            def __init_subclass__(cls):
                cls.y = 1
            ns['__init_subclass__'] = __init_subclass__
        BaseF = types.new_class("BaseF", (C,), exec_body=f)
        F = types.new_class("F", (BaseF,))
        self.assertEqual(F.y, 1)
        self.assertEqual(F.x, 0)
        self.assertNotIn('x', F.__dict__)
        self.assertFalse(hasattr(C, 'y'))
        # __init_subclass__ raises an exception:
        def s(ns):
            def __init_subclass__(cls):
                raise KeyError('xxx')
            ns['__init_subclass__'] = __init_subclass__
        S = sentinel = object()
        with self.assertRaisesRegex(KeyError, 'xxx'):
            BaseS = types.new_class("BaseS", (Object,), exec_body=s)
            S = types.new_class("S", (BaseS,))
        self.assertIs(S, sentinel)

    def test_args(self):
        with self.assertRaises(TypeError):
            class C(Object, some_arg=4):
                pass

        class Base(Object):
            def __init_subclass__(cls, some_arg, **kwargs):
                super().__init_subclass__(**kwargs)
                cls.store_arg = some_arg

        class A(Base, some_arg=3):
            pass

        self.assertEqual(A.store_arg, 3)

        with self.assertRaises(TypeError):
            class B(Base):
                pass


    def test_namespace(self):
        class Class(Object):
            a = 1
            def b(self):
                pass
            c = 3
        self.assertEqual(Class.__attribute_order__,
                         ("__module__", "__qualname__", "a", "b", "c"))

    def test_descriptor(self):
        class Descriptor:
            def __set_owner__(self, owner, name):
                self.name = name
                self.owner = owner

        class NoDescriptor:
            pass

        class Class(Object):
            d = Descriptor()
            nd = NoDescriptor()

        self.assertEqual(Class.d.name, "d")
        self.assertIs(Class.d.owner, Class)

    def test_abc(self):
        class Base(abc.ABC):
            @abc.abstractmethod
            def f(self):
                pass

        class Incomplete(Base, ABC):
            pass

        class Complete(Incomplete):
            def f(self):
                pass

        with self.assertRaises(TypeError):
            a = Incomplete()
        b = Complete()


if __name__ == "__main__":
    main()
