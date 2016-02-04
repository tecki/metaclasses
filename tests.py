from metaclass import SubclassInit, Meta
from unittest import TestCase, main
import types

class Test(TestCase):
    def test_classes(self):
        # PEP 422: Simple class initialisation hook
        class BaseC(SubclassInit):
            def __init_subclass__(cls, ns):
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
            def __init_subclass__(cls, ns):
                cls.y = 1
        class F(BaseF):
            pass
        self.assertEqual(1, F.y)
        self.assertEqual(0, F.x)
        self.assertNotIn('x', F.__dict__)
        self.assertFalse(hasattr(C, 'y'))
        # super:
        class BaseG(C):
            def __init_subclass__(cls, ns):
                super().__init_subclass__(ns)
                cls.y = 1
        class G(BaseG):
            pass
        self.assertEqual(1, G.y)
        self.assertEqual(0, G.__dict__['x'])
        self.assertFalse(hasattr(C, 'y'))
        # __class__:
        class BaseI(SubclassInit):
            def __init_subclass__(cls, ns):
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
            def __init_subclass__(cls, ns):
                super().__init_subclass__(ns)
                __class__.z += 1
            z = 0
        class K(BaseK):
            pass
        self.assertEqual(0, K.__dict__['x'])
        self.assertEqual(4, I.y)
        self.assertEqual(1, K.z)
        self.assertFalse(hasattr(J, 'z'))
        # multiple inheritance:
        class L(SubclassInit):
            def __init_subclass__(cls, ns):
                pass
        class BaseM(L):
            def __init_subclass__(cls, ns):
                super().__init_subclass__(ns)
                cls.x = 0
        class M(BaseM):
            pass
        self.assertEqual(0, M.x)
        class BaseN(L):
            def __init_subclass__(cls, ns):
                super().__init_subclass__(ns)
                cls.y = 1
        class N(BaseN):
            pass
        self.assertEqual(1, N.y)
        class BaseO(M, N):
            def __init_subclass__(cls, ns):
                super().__init_subclass__(ns)
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
            def __init_subclass__(cls, ns):
                cls.x = 0
        self.assertEqual(2, P.x)
        # __init_subclass__ raises an exception:
        S = sentinel = object()
        with self.assertRaisesRegex(KeyError, 'xxx'):
            class BaseS(SubclassInit):
                def __init_subclass__(cls, ns):
                    raise KeyError('xxx')
            class S(BaseS):
                pass
        self.assertIs(sentinel, S)

    def test_types(self):
        # PEP 422: Simple class initialisation hook
        def c(ns):
            def __init_subclass__(cls, ns):
                cls.x = 0
            ns['__init_subclass__'] = __init_subclass__
        BaseC = types.new_class("BaseC", (SubclassInit,), exec_body=c)
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
            def __init_subclass__(cls, ns):
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
            def __init_subclass__(cls, ns):
                raise KeyError('xxx')
            ns['__init_subclass__'] = __init_subclass__
        S = sentinel = object()
        with self.assertRaisesRegex(KeyError, 'xxx'):
            BaseS = types.new_class("BaseS", (SubclassInit,), exec_body=s)
            S = types.new_class("S", (BaseS,))
        self.assertIs(S, sentinel)

    def test_namespace(self):
        outer = self
        class NS(dict):
            def __init__(self):
                super().__init__(bar=3)
            def __setitem__(self, attr, value):
                if not attr.startswith("__"):
                    NS.called_set = True
                    outer.assertEqual(attr, "spam")
                    outer.assertEqual(value, "ham")
                super().__setitem__(attr, value)
            def __getitem__(self, attr):
                if not attr.startswith("__"):
                    NS.called_get = True
                    outer.assertIn(attr, ("outer", "bar"))
                return super().__getitem__(attr)
        class Base(SubclassInit, namespace=NS):
            pass
        class Class(Base):
            outer.assertEqual(bar, 3)
            spam = "ham"
        self.assertTrue(NS.called_set)
        self.assertTrue(NS.called_get)

    def test_descriptor(self):
        class Descriptor:
            def __init_descriptor__(self, owner, name):
                self.name = name
                self.owner = owner

        class NoDescriptor:
            pass

        class Class(SubclassInit):
            d = Descriptor()
            nd = NoDescriptor()

        self.assertEqual(Class.d.name, "d")
        self.assertIs(Class.d.owner, Class)


if __name__ == "__main__":
    main()
