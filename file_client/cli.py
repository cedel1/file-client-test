import click

from .backend_clients import (
    GRPCClient, RESTClient, DEFAULT_STDOUT_PRINT_MARKER)


class Context(object):

    def __init__(self):
        pass


pass_context = click.make_pass_decorator(Context, ensure=True)


def get_client(context):
    if context.backend == 'grpc':
        return GRPCClient(context)
    elif context.backend == 'rest':
        return RESTClient(context)
    else:
        raise ValueError('Backend not supported')


@click.group()
@click.version_option()
@click.option(
    '--backend',
    default='grpc',
    type=click.Choice(['grpc', 'rest']),
    help='Set a backend to be used, choises are grpc and rest. Default is grpc',
)
@click.option(
    '--grpc-server',
    default='localhost:50051',
    type=click.UNPROCESSED,
    metavar='NETLOC',
    help='Set a host and port of the gRPC server. Default is localhost:50051',
)
@click.option(
    '--base-url',
    default='http://localhost/',
    type=click.UNPROCESSED,
    metavar='URL',
    help='Set a base URL for a REST server. Default is http://localhost/.',
)
@click.option(
    '--output',
    default=DEFAULT_STDOUT_PRINT_MARKER,
    type=click.File('w'),
    metavar='OUTPUT',
    help='Set the file where to store the output. Default is -, i.e. the' \
        ' stdout.',
)
@pass_context
def cli(context, backend, grpc_server, base_url, output):
    """
    CLI application which retrieves and prints data from one of the described
    backends.
    """
    context.backend = backend
    context.grpc_server = grpc_server
    context.base_url = base_url
    context.output = output


@cli.command(name='stat')
@click.argument(
    'UUID'
)
@pass_context
def stat(context, uuid):
    'Prints the file metadata in a human-readable manner.'
    #click.echo('Here is some output from stat')
    client = get_client(context)
    client.stat_and_output(uuid)


@cli.command(name='read')
@click.argument(
    'UUID'
)
@pass_context
def read(context, uuid):
    'Outputs the file content.'
    client = get_client(context)
    client.read_and_output(uuid)
