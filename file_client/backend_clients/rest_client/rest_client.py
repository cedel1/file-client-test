from urllib.parse import quote, urljoin

import requests

from ..client import Client
from ..client_exceptions import (ClientException, ClientExceptionFileNotFound,
                                 ClientExceptionInvalidURL)


class RESTClient(Client):

    def read(self, uuid):
        """
        ``file/<uuid>/read/``
        =====================
        Accepts a ``GET`` requests.
        Returns a response with the file contents.
        A ``Content-Disposition`` header contains a display name of the file.
        A ``Content-Type`` header contains a MIME type of the file.

        If a file is not found, HTTP code 404 is returned.
        """
        try:
            with requests.get(
                self._sanitize_url(self.base_url, f'file/{uuid}/read/')
            ) as response:
                response.raise_for_status()
                return (
                    response.content,
                    response.headers.get('Content-Disposition'),
                    response.headers.get('Content-Type')
                )
        except (requests.exceptions.RequestException) as e:
            self._process_http_error(e)

    def stat(self, uuid):
        """
        ``file/<uuid>/stat/``
        =====================
        Accepts a ``GET`` requests.
        Returns a JSON response with an file metadata in a JSON object.
        A file metadata contains following keys:

        * ``create_datetime`` - File creation date and time in ISO format
        * ``size`` - File size in bytes
        * ``mimetype`` - File MIME type
        * ``name`` - Display name of the file

        If a file is not found, HTTP code 404 is returned.
        """
        try:
            with requests.get(
                self._sanitize_url(self.base_url, f'file/{uuid}/stat/')
            ) as response:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.JSONDecodeError:
            raise ClientException('The file returned is not a valid JSON.')
        except (requests.exceptions.RequestException) as e:
            self._process_http_error(e)

    def _process_http_error(self, exception):
        if isinstance(exception, requests.exceptions.MissingSchema):
            raise ClientExceptionInvalidURL(exception)
        elif (
            isinstance(exception, requests.exceptions.HTTPError)
            and exception.response.status_code == 404
        ):
            raise ClientExceptionFileNotFound()
        else:
            raise ClientException(exception)

    def _sanitize_url(self, base_url, path):
        return quote(urljoin(base_url, path), safe="/:@")
