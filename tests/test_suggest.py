import unittest
from pytsdb import tsdb
from pytsdb import errors
from unittest import mock
from tests.testutils import get_mock_requests_post, mock_tsdb_connection_error_post, mock_unexpected_error_post
from tests.testutils import ADHOC_HOSTS, ADHOC_PORTS, ADHOC_PROTOCOLS


class SuggestTestCase(unittest.TestCase):

    __TEST_RESPONSE__ = [
        "sys.unix.v0",
        "sys.linux.v0",
        "sys.win.v0",
    ]

    def setUp(self):
        self._host = 'localhost'
        self._port = 5896
        self._protocol = 'mockhttp'

        self._c = tsdb.tsdb_connection(self._host, self._port, protocol=self._protocol)

    @mock.patch('requests.post', side_effect=get_mock_requests_post(None))
    def test_url(self, _):
        hosts = ADHOC_HOSTS
        ports = ADHOC_PORTS
        protocols = ADHOC_PROTOCOLS

        for a, b, c in zip(hosts, ports, protocols):
            expected_url = '{}://{}:{}/api/suggest/'.format(c, a, b)
            self._c = tsdb.tsdb_connection(a, b, protocol=c)
            mock_return_value = self._c.suggest(type="metric")
            # url is added ad hoc in testutils
            self.assertTrue(mock_return_value[-1] == expected_url)

    @mock.patch('requests.post', side_effect=get_mock_requests_post(__TEST_RESPONSE__))
    def test_suggest(self, _):
        return_value = self._c.suggest(type="metric")
        self.assertEqual(sorted(return_value), sorted(SuggestTestCase.__TEST_RESPONSE__))

    @mock.patch('requests.post', side_effect=get_mock_requests_post(None))
    def test_suggest_missing_type(self, _):
        with self.assertRaises(Exception) as context:
            self._c.suggest()
        self.assertTrue(isinstance(context.exception, errors.MissingArgumentError))

    @mock.patch('requests.post', side_effect=mock_tsdb_connection_error_post)
    def test_suggest_tsdberror(self, _):
        with self.assertRaises(Exception) as context:
            self._c.suggest(type="metric")
        self.assertTrue(isinstance(context.exception, errors.TsdbConnectionError))

    @mock.patch('requests.post', side_effect=mock_unexpected_error_post)
    def test_suggest_unexpectederror(self, _):
        with self.assertRaises(Exception) as context:
            self._c.suggest(type="metric")
        self.assertTrue(isinstance(context.exception, errors.UncaughtError))

    @mock.patch('requests.post', side_effect=get_mock_requests_post(
        response_content={"error": {"message": "Response code differ 200"}}, status_code=403))
    def test_suggest_403(self, _):
        with self.assertRaises(Exception) as context:
            self._c.suggest(type="metric")
        self.assertTrue(isinstance(context.exception, errors.UncaughtError))

    @mock.patch('requests.post', side_effect=get_mock_requests_post(
        response_content={"error": {"message": "Response code differ 200"}}, status_code=400))
    def test_suggest_400(self, _):
        with self.assertRaises(Exception) as context:
            self._c.suggest(type="metric")
        self.assertTrue(isinstance(context.exception, errors.ArgumentError))