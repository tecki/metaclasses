# metaclasses
Some ideas about improving metaclasses.
PEP 422 is a proposal to have a replacement for metaclasses.
pep422.py implements something like that, using metaclasses.

The difference is that instead of having an initializer for
a class, one defines initializers for all subclasses.

An example of usage can be found in example.py.
