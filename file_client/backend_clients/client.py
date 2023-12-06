from abc import ABC, abstractmethod
from typing import Any, Dict


DEFAULT_STDOUT_PRINT_MARKER = '-'


class Client(ABC):

    def __init__(self, context):
        self.backend = context.backend
        self.grpc_server = context.grpc_server
        self.base_url = context.base_url
        self.output = context.output

    @abstractmethod
    def read(self, uuid) -> (bytes, str, str):
        raise NotImplementedError

    @abstractmethod
    def stat(self, uuid) -> Dict[str, Any]:
        raise NotImplementedError

    def read_and_output(self, uuid):
        content, _, content_type = self.read(uuid)
        self.output_result(self._print_content(content, content_type), content)

    def stat_and_output(self, uuid):
        resulting_text = self._process_dict_for_display(self.stat(uuid))
        self.output_result(resulting_text, resulting_text, file_flags='wt')

    def output_result(self, print_output, file_output, file_flags='wb'):
        if self.output == DEFAULT_STDOUT_PRINT_MARKER:
            print(print_output)
        else:
            with open(self.output, file_flags) as file:
                file.write(file_output)

    def _print_content(self, content, content_type=None):
        # This is quite a hack. It would probably by better to just print
        # the content in bytes in every case.
        if (
            content_type
            and ('text/' in content_type or 'json/' in content_type)
        ):
                return content.decode()
        else:
            return content

    def _process_dict_for_display(self, attributes_dict):
        # This displays present json keys. If displaying even missing keys
        # and no possible extra keys was required, it could be added
        # for example by iterating over a set of required keys and displaying
        # their values or 'Not present' default value,
        # like so (untested approximation):
        #
        # keys = {'key1', 'key2', 'key3'}
        # return '\n'.join(
        #     [f'{key}: {value}' for key, value in [
        #         (key, attributes_dict.get(key, 'Not present'))
        #         for key in keys]]
        # )
        return '\n'.join(
            [f'{key}: {value}' for key, value in attributes_dict.items()]
        )
