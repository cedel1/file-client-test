import pytest
from file_client.cli import Context
from file_client.backend_clients.client import Client


@pytest.fixture
def context():
    context = Context()
    context.backend = 'grpc'
    context.grpc_server = 'localhost:50051'
    context.base_url = 'http://localhost/'
    context.output = '-'
    return context


@pytest.fixture
def concrete_client_without_context():
    """
    This fixture is a workaround for not being able to instantiate an abstract
    class, that still has to be tested.
    """
    class TestingClient(Client):
        pass
    TestingClient.__abstractmethods__ = frozenset()
    return type('DummyConcrete' + Client.__name__, (TestingClient, ), {})


@pytest.fixture
def concrete_client(context, concrete_client_without_context):
    return concrete_client_without_context(context)


@pytest.fixture
def tmp_file(tmp_path):
    return tmp_path / 'testing_output.txt'
