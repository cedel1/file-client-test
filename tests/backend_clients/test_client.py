import pytest
from tests.helpers.fixtures import (
    context, concrete_client_without_context, concrete_client, tmp_file)  # noqa 401
from unittest.mock import MagicMock


def test_abstract_client_read_method_should_return_not_implemented(
        concrete_client):
    with pytest.raises(NotImplementedError):
        concrete_client.read('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')


def test_abstract_client_stat_method_should_return_not_implemented(
        concrete_client):
    with pytest.raises(NotImplementedError):
        concrete_client.stat('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')


def test_abstract_client_read_and_output_should_call_read_and_output_result(
        concrete_client):
    mocked_read = MagicMock(return_value=(b'content read', 'str1', 'str2'))
    mocked_output_result = MagicMock()
    concrete_client.read = mocked_read
    concrete_client.output_result = mocked_output_result
    concrete_client.read_and_output('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')
    assert mocked_read.call_count == 1
    assert mocked_output_result.call_count == 1


def test_abstract_client_stat_and_output_should_call_stat_and_output_result(
        concrete_client):
    mocked_stat = MagicMock(return_value=({'key1': 'val1', 'key2': 10}))
    mocked_output_result = MagicMock()
    concrete_client.stat = mocked_stat
    concrete_client.output_result = mocked_output_result
    concrete_client.stat_and_output('1f2b5c6e-3d4e-5f6g-7h8i-9j0k1l2m3n4o')
    assert mocked_stat.call_count == 1
    assert mocked_output_result.call_count == 1


def test_abstract_client_output_method_should_print_result_by_default(
        concrete_client, capfd):
    assert concrete_client.output == '-'
    concrete_client.output_result('testing output', 'testing output')
    out, _ = capfd.readouterr()
    assert out == 'testing output\n'


def test_abstract_client_output_method_should_save_to_file_provided(
        context, concrete_client_without_context, capfd, tmp_file):
    context.output = tmp_file
    client = concrete_client_without_context(context)
    assert client.output == tmp_file
    client.output_result(
        'testing output',
        bytes('testing output'.encode('utf-8')))
    out, err = capfd.readouterr()
    assert out == ''
    assert err == ''
    with open(tmp_file, 'rt') as file:
        assert file.read() == 'testing output'


@pytest.mark.parametrize(
    'attributes, expected_result', [
        ({'attribute1': 'value1', 'attribute2': 'value2', 'att3': 10},
         'attribute1: value1\nattribute2: value2\natt3: 10'
         ),
    ]
)
def test_process_dict_for_display_should_join_dict_in_a_correct_way(
        concrete_client, attributes, expected_result):
    assert (
        concrete_client._process_dict_for_display(attributes)
        == expected_result
    )
