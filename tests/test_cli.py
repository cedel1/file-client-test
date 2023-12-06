from click.testing import CliRunner
from file_client.cli import cli, get_client
from .helpers.fixtures import context  # noqa 401
from file_client.backend_clients import GRPCClient, RESTClient
import pytest


def test_version_commend_should_return_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert result.output.startswith('cli, version ')


def test_help_command_should_return_help():
    required_help_strings = (
        'Usage: cli [OPTIONS] COMMAND [ARGS]...',
        'CLI application which retrieves and prints data from one of the ' \
        'described\n  backends.',
        'Options:',
        '--version              Show the version and exit.',
        '--backend [grpc|rest]  Set a backend to be used, choises are grpc ' \
        'and rest.',
        'Default is grpc',
        '--grpc-server NETLOC   Set a host and port of the gRPC server. ' \
        'Default is',
        'localhost:50051',
        '--base-url URL         Set a base URL for a REST server. Default is',
        'http://localhost/',
        '--output OUTPUT        Set the file where to store the output. ' \
        'Default is -,',
        'i.e. the stdout.',
        '--help                 Show this message and exit.',
        'Commands:',
        'read  Outputs the file content.',
        'stat  Prints the file metadata in a human-readable manner.',
        )
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        for required_help_text in required_help_strings:
            assert required_help_text in result.output


@pytest.mark.parametrize(
    'context_backend_marker, client_class', [
        ('grpc', GRPCClient),
        ('rest', RESTClient),
    ]
)
def test_get_client_should_return_correct_client(
        context, context_backend_marker, client_class):
    context.backend = context_backend_marker
    assert isinstance(get_client(context), client_class)


def test_get_client_should_raise_value_error_if_incorrect_client_provided(
        context):
    context.backend = 'nonexistent-backend'
    with pytest.raises(ValueError) as error:
        get_client(context)
    assert str(error.value) == 'Backend not supported'
