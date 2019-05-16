pytest_plugins = 'pytester'
from pytest_aloe import step
import pytest
from aloe import world

@pytest.fixture
def test_get_request(request):
    return request

@step(r'I have a foo fixture with value "([^"]*)"')
def foo(self, arg, bar):    
    print("\nfoo executed");

@step(r'there is a list')
def foo2(self):
    print("foo2 executed");
