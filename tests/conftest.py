pytest_plugins = 'pytester'
from pytest_aloe import step

@step(r'I have a foo fixture with value "([^"]*)"')
def foo(self, arg):
    print("executed");

@step(r'there is a list')
def foo2(self):
    print("executed");