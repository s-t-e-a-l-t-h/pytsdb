import unittest
from pytsdb import pytsdb
from unittest import mock
from tests.testutils import mock_requests_get


class TsdbConfigTestCase(unittest.TestCase):

    def setUp(self):
        self._host = 'localhost'
        self._port = 5896
        self._protocol = 'mockhttp'

        self._hosts = ['localhost', 'myqeb.com', 'web.kim.com']
        self._ports = ['201', 22222, 693]
        self._protocols = ['http', 'https', 'ftp']

        self._c = pytsdb.connect(self._host, self._port, protocol=self._protocol)

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_config_url(self, _):

        for a, b, c in zip(self._hosts, self._ports, self._protocols):
            expected_url = '{}://{}:{}/api/config/'.format(c, a, b)
            self._c = pytsdb.connect(a, b, protocol=c)
            mock_return_value = self._c.config()

            self.assertTrue(isinstance(mock_return_value, dict))
            self.assertTrue(mock_return_value.get('url') == expected_url)

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_filters_url(self, _):
        for a, b, c in zip(self._hosts, self._ports, self._protocols):
            expected_url = '{}://{}:{}/api/config/filters/'.format(c, a, b)
            self._c = pytsdb.connect(a, b, protocol=c)
            mock_return_value = self._c.filters()

            self.assertTrue(isinstance(mock_return_value, dict))
            self.assertTrue(mock_return_value.get('url') == expected_url)