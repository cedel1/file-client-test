import pytest
import requests
import responses
from click.testing import CliRunner
from file_client.backend_clients.client_exceptions import (
    ClientException, ClientExceptionFileNotFound, ClientExceptionInvalidURL)
from file_client.backend_clients.rest_client.rest_client import RESTClient
from file_client.cli import cli
from tests.helpers.fixtures import context  # noqa: F401
from unittest.mock import MagicMock
import json


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps



@pytest.mark.parametrize(
    'base_url, uuid, expected_value', [
        ('http://one_base_url/',
         '1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o',
         'http://one_base_url/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/read/'),
        ('https://localhost',
         'e6b8c3dc-0b34-4a6a-9489-659b1d8c17f6',
         'https://localhost/file/e6b8c3dc-0b34-4a6a-9489-659b1d8c17f6/read/'),
        ('http://localhost:5051',
         '3a7abf7f-2907-44e4-bc52-1b7d8b0e0c3e',
         'http://localhost:5051/file/3a7abf7f-2907-44e4-bc52-1b7d8b0e0c3e/read/'
         ),
    ]
)
def test_rest_client_read_method_should_call_correct_url(
        base_url, uuid, expected_value, mocked_responses):
    runner = CliRunner()
    with runner.isolated_filesystem():
        response = mocked_responses.get(
            expected_value,
            body=b'',
            status=200,
        )

        runner.invoke(
            cli,
            f'--backend rest --base-url {base_url} read {uuid}'
            )
        assert response.call_count == 1


@pytest.mark.parametrize(
    'base_url, uuid, expected_value', [
        ('http://one_base_url/',
         '1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o',
         'http://one_base_url/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/stat/'),
        ('https://localhost',
         'e6b8c3dc-0b34-4a6a-9489-659b1d8c17f6',
         'https://localhost/file/e6b8c3dc-0b34-4a6a-9489-659b1d8c17f6/stat/'),
        ('http://localhost:5051',
         '3a7abf7f-2907-44e4-bc52-1b7d8b0e0c3e',
         'http://localhost:5051/file/3a7abf7f-2907-44e4-bc52-1b7d8b0e0c3e/stat/'
         ),
    ]
)
def test_rest_client_stat_method_should_call_correct_url(
        base_url, uuid, expected_value, mocked_responses):

    runner = CliRunner()
    with runner.isolated_filesystem():
        response = mocked_responses.get(
            expected_value,
            body=b'',
            status=200,
        )

        runner.invoke(
            cli,
            f'--backend rest --base-url {base_url} stat {uuid}'
            )
        assert response.call_count == 1


def test_rest_client_should_exit_on_invalid_base_url(
        mocked_responses):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            '--backend rest --base-url "localhost" read '
            '1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o',
            )
        assert result.exit_code == 1
        assert isinstance(result.exception, ClientExceptionInvalidURL)


@pytest.mark.parametrize(
    'base_url, url, expected_value', [
        ('local;host',
         'file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/read/',
         'file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/read/'),
        ('http://local;host',
         'file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/read/',
         'http://local%3Bhost/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/read/',
         ),
        ('http://root@someotherhost',
         'some_url',
         'http://root@someotherhost/some_url'
         ),
        ('https://root@someotherhost',
         '/some_url; sudo rm /',
         'https://root@someotherhost/some_url%3B%20sudo%20rm%20/'
         ,)
    ]
)
def test_sanitize_url_should_remove_unwanted_characters_from_url(
        context, base_url, url, expected_value):
    client = RESTClient(context)
    client.base_url = base_url
    assert expected_value == client._sanitize_url(base_url, url)


def test_process_http_error_should_raise_client_exception_if_url_invalid(
        context, capfd):
    client = RESTClient(context)
    exception = requests.exceptions.MissingSchema()
    with pytest.raises(ClientExceptionInvalidURL):
        client._process_http_error(exception)
    out, _ = capfd.readouterr()
    assert out == 'Invalid URL was entered. \n'


def test_process_http_error_should_raise_client_exception_file_not_found(
        context, capfd):
    client = RESTClient(context)
    exception = requests.exceptions.HTTPError(response=requests.Response())
    exception.response.status_code = 404
    with pytest.raises(ClientExceptionFileNotFound):
        client._process_http_error(exception)
    out, _ = capfd.readouterr()
    assert out == 'File was not found on the remote server. \n'


def test_process_http_error_should_raise_client_exception_if_not_404(
        context, capfd):
    client = RESTClient(context)
    exception = requests.exceptions.HTTPError(response=requests.Response())
    with pytest.raises(ClientException):
        client._process_http_error(exception)
    out, _ = capfd.readouterr()
    assert out == 'An unexpected client exception occured. More details: \n'


def test_process_http_error_should_raise_client_exception_if_not_HTTPError(
        context, capfd):
    client = RESTClient(context)
    exception = requests.exceptions.Timeout(response=requests.Response())
    exception.response.status_code = 404
    with pytest.raises(ClientException):
        client._process_http_error(exception)
    out, _ = capfd.readouterr()
    assert out == 'An unexpected client exception occured. More details: \n'


def test_client_rest_stat_should_raise_exception_on_invalid_json(
        context, mocked_responses, capfd):
    client = RESTClient(context)
    with pytest.raises(ClientException) as exception_info:
        mocked_responses.get(
            'http://localhost/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/stat/',
            body=b'neco',
            status=200,
        )
        client.stat('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')
    out, _ = capfd.readouterr()

    assert str(exception_info.value) == 'The file returned is not a valid JSON.'
    assert out == (
        'An unexpected client exception occured. More details: The file '
        'returned is not a valid JSON.\n'
    )


def test_client_rest_should_call_process_http_errors_on_some_exceptions(
        context, mocked_responses):
    client = RESTClient(context)
    mock = MagicMock()
    client._process_http_error = mock
    mocked_responses.get(
        'http://localhost/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/stat/',
        body='',
        status=404,
    )
    mocked_responses.get(
        'http://localhost/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/read/',
        body='',
        status=404,
    )
    client.stat('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')
    assert mock.call_count == 1
    client.read('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')
    assert mock.call_count == 2


@pytest.mark.parametrize(
    'body_dict', [
        {'create_datetime': '2020-01-01T00:00:00Z',
         'size': 12345,
         'mimetype': 'text/plain',
         'name': 'file.txt',
         },
        {'create_datetime': '2020-01-01',
         'size': None,
         'mimetype': 'application/json',
         'name': 'test.json',
         },
    ]
)
def test_rest_client_stat_should_return_correct_file_metadata(
        context, mocked_responses, body_dict):
    client = RESTClient(context)
    mocked_responses.get(
        'http://localhost/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/stat/',
        body=json.dumps(body_dict),
        status=200,
    )
    result = client.stat('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')
    assert result == body_dict


@pytest.mark.parametrize(
    'file_content, content_disposition, content_type', [
        (b'content',  # response.content always returns bytes
         'attachment; filename="file.pdf"',
         'application/pdf; charset=utf-8'
         ),
        (b'content',
         'attachment; filename="file.pdf"',
         'text/plain; charset=utf-8'
         ),
        (b'text file content',
         'inline; filename="file.txt"',
         'text/plain; charset=iso-8859-2'
         ),
    ]
)
def test_rest_client_read_should_return_correct_file_content(
        context, mocked_responses, file_content, content_disposition,
        content_type):
    client = RESTClient(context)
    mocked_responses.get(
        'http://localhost/file/1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o/read/',
        body=file_content,
        status=200,
        headers={
            'Content-Disposition': content_disposition,
            'Content-Type': content_type
        },
    )
    result = client.read('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')
    assert result == (file_content, content_disposition, content_type)
