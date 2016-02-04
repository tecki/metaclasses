from metaclass import SubclassInit

class AttributeOrder(SubclassInit):
    a = 1

    def b(self):
        pass

    c = 5

assert AttributeOrder.__attribute_order__ == \
    ('__module__', '__qualname__', 'a', 'b', 'c')

